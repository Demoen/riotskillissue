import asyncio
import logging
from typing import Optional, Any

import httpx
from tenacity import (
    retry,
    wait_exponential,
    retry_if_exception_type,
    stop_after_attempt,
)

from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.types import Region, Platform
from riotskillissue.core.ratelimit import (
    AbstractRateLimiter,
    MemoryRateLimiter,
    RedisRateLimiter,
    parse_rate_limits,
)
from riotskillissue.core.cache import AbstractCache, NoOpCache

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class RiotAPIError(Exception):
    """Base exception for all Riot API errors."""

    def __init__(self, status: int, message: str, response: httpx.Response):
        self.status = status
        self.message = message
        self.response = response
        super().__init__(f"[{status}] {message}")


class BadRequestError(RiotAPIError):
    """400 – The request was malformed."""

    def __init__(self, response: httpx.Response):
        super().__init__(400, response.text, response)


class UnauthorizedError(RiotAPIError):
    """401 – Missing or invalid API key."""

    def __init__(self, response: httpx.Response):
        super().__init__(401, "Unauthorized – check your API key", response)


class ForbiddenError(RiotAPIError):
    """403 – Insufficient permissions for this endpoint."""

    def __init__(self, response: httpx.Response):
        super().__init__(403, "Forbidden – insufficient permissions", response)


class NotFoundError(RiotAPIError):
    """404 – The requested resource was not found."""

    def __init__(self, response: httpx.Response):
        super().__init__(404, "Not Found", response)


class RateLimitError(RiotAPIError):
    """429 – Rate limited.  ``retry_after`` gives the recommended wait."""

    def __init__(self, response: httpx.Response, retry_after: float):
        super().__init__(429, f"Rate limited. Retry after {retry_after}s", response)
        self.retry_after = retry_after


class ServerError(RiotAPIError):
    """5xx – Riot server-side error."""
    pass


# Map status codes to specialised error classes
_STATUS_ERROR_MAP = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
}


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------

class HttpClient:
    def __init__(
        self,
        config: RiotClientConfig,
        rate_limiter: Optional[AbstractRateLimiter] = None,
        cache: Optional[AbstractCache] = None,
        hooks: Optional[dict] = None,
    ):
        self.config = config
        self.cache = cache or NoOpCache()
        self.hooks = hooks or {}
        self._client = httpx.AsyncClient(
            headers={
                "X-Riot-Token": config.api_key,
                # Explicitly disable compressed responses. Python 3.13+ ships
                # with zlib-ng whose deflate/gzip decoder can choke on some Riot
                # API responses ("Error -3 while decompressing data: incorrect
                # header check"). Requesting identity avoids the problem at a
                # negligible bandwidth cost for JSON payloads.
                "Accept-Encoding": "identity",
            },
            timeout=httpx.Timeout(
                config.read_timeout,
                connect=config.connect_timeout,
            ),
            proxy=config.proxy,
        )

        # Rate limiter selection
        if rate_limiter:
            self.limiter = rate_limiter
        elif config.redis_url:
            self.limiter = RedisRateLimiter(config.redis_url)
        else:
            self.limiter = MemoryRateLimiter()

        # Default rate-limit buckets per Riot's default application limits.
        # These will be updated dynamically from response headers.
        self._default_limits = parse_rate_limits("20:1,100:120")

    async def close(self) -> None:
        await self._client.aclose()

    # -- public entry point --------------------------------------------------

    async def request(
        self,
        method: str,
        url: str,
        region_or_platform: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Execute a request with caching, rate limiting, and retries."""

        # 1. Cache check (GET only)
        cache_key: Optional[str] = None
        if method.upper() == "GET":
            cache_key = self._cache_key(method, url, region_or_platform, kwargs)
            cached = await self.cache.get(cache_key)
            if cached is not None:
                status, headers, content = cached
                return httpx.Response(
                    status_code=status, headers=headers, content=content
                )

        # 2. Hook: onRequest
        if "request" in self.hooks:
            await self.hooks["request"](method, url, kwargs)

        # 3. Execute with retry (rate-limiting happens inside)
        response = await self._execute_with_retry(
            method, url, region_or_platform, **kwargs
        )

        # 4. Hook: onResponse
        if "response" in self.hooks:
            await self.hooks["response"](response)

        # 5. Cache set (only successful GETs)
        if method.upper() == "GET" and response.status_code == 200:
            if cache_key is None:
                cache_key = self._cache_key(method, url, region_or_platform, kwargs)
            await self.cache.set(
                cache_key,
                (response.status_code, dict(response.headers), response.content),
                ttl=self.config.cache_ttl,
            )

        return response

    # -- internals -----------------------------------------------------------

    @staticmethod
    def _cache_key(method: str, url: str, region: str, kwargs: Any) -> str:
        params = kwargs.get("params", {})
        param_key = str(sorted(params.items())) if params else ""
        return f"{method}:{url}:{region}:{param_key}"

    async def _execute_with_retry(
        self, method: str, url: str, key: str, **kwargs: Any
    ) -> httpx.Response:
        """Retry loop that handles transient errors *and* 429 back-off."""

        # Normalise enum values so the host is always a plain string
        # (on Python <3.11 str(StrEnum.X) returns "ClassName.X")
        if hasattr(key, "value"):
            key = key.value

        max_attempts = self.config.max_retries
        attempt = 0

        while True:
            attempt += 1

            # ---- Rate limit acquisition ------------------------------------
            limiter_key = f"{key}:{method}:{url}"
            await self.limiter.acquire(limiter_key, self._default_limits)

            # ---- Build full URL --------------------------------------------
            if not url.startswith("https://"):
                if self.config.base_url:
                    host = self.config.base_url.rstrip("/")
                else:
                    host = f"https://{key}.api.riotgames.com"
                full_url = f"{host}{url}"
            else:
                full_url = url

            try:
                response = await self._client.request(method, full_url, **kwargs)
            except (
                httpx.NetworkError,
                httpx.TimeoutException,
                httpx.RemoteProtocolError,
            ) as exc:
                logger.warning("Network error accessing %s: %s", full_url, exc)
                if attempt >= max_attempts:
                    raise
                wait = min(2 ** attempt, 10)
                logger.debug("Retrying in %.1fs (attempt %d/%d)", wait, attempt, max_attempts)
                await asyncio.sleep(wait)
                continue

            # ---- Status-code handling --------------------------------------

            # 429 – sleep for Retry-After then retry (does NOT count against max_attempts)
            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", "1"))
                logger.warning(
                    "Rate limited (429) on %s. Sleeping %.1fs.", key, retry_after
                )
                await asyncio.sleep(retry_after)
                continue

            # 5xx – transient server error, retry with back-off
            if response.status_code >= 500:
                logger.warning("Server error %d on %s", response.status_code, key)
                if attempt >= max_attempts:
                    raise ServerError(response.status_code, "Server Error", response)
                wait = min(2 ** attempt, 10)
                await asyncio.sleep(wait)
                continue

            # 4xx – deterministic client errors, raise immediately
            if not response.is_success:
                err_cls = _STATUS_ERROR_MAP.get(response.status_code)
                if err_cls:
                    raise err_cls(response)
                raise RiotAPIError(response.status_code, response.text, response)

            # ---- Update rate-limit state from response headers -------------
            app_limits = response.headers.get("X-App-Rate-Limit")
            app_counts = response.headers.get("X-App-Rate-Limit-Count")
            if app_limits:
                self._default_limits = parse_rate_limits(app_limits)
            if app_counts:
                await self.limiter.update(limiter_key, app_counts, app_limits)

            return response
