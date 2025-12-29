import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional, Any, AsyncGenerator

import httpx
from tenacity import retry, wait_exponential, retry_if_exception_type, stop_after_attempt

from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.types import Region, Platform
from riotskillissue.core.ratelimit import AbstractRateLimiter, MemoryRateLimiter, RedisRateLimiter
from riotskillissue.core.cache import AbstractCache, NoOpCache

logger = logging.getLogger(__name__)

class RiotAPIError(Exception):
    def __init__(self, status: int, message: str, response: httpx.Response):
        self.status = status
        self.message = message
        self.response = response
        super().__init__(f"[{status}] {message}")

class RateLimitError(RiotAPIError):
    def __init__(self, response: httpx.Response, retry_after: float):
        super().__init__(429, f"Rate limited. Retry after {retry_after}s", response)
        self.retry_after = retry_after

class ServerError(RiotAPIError):
    pass

class HttpClient:
    def __init__(self, config: RiotClientConfig, rate_limiter: Optional[AbstractRateLimiter] = None, cache: Optional[AbstractCache] = None, hooks: Optional[dict] = None):
        self.config = config
        self.cache = cache or NoOpCache()
        self.hooks = hooks or {}
        self._client = httpx.AsyncClient(
            headers={"X-Riot-Token": config.api_key},
            timeout=httpx.Timeout(
                config.read_timeout, 
                connect=config.connect_timeout
            ),
        )
        if rate_limiter:
            self.limiter = rate_limiter
        elif config.redis_url:
            self.limiter = RedisRateLimiter(config.redis_url)
        else:
            self.limiter = MemoryRateLimiter()

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self, 
        method: str, 
        url: str, 
        region_or_platform: str, 
        **kwargs: Any
    ) -> httpx.Response:
        """
        Executes a request with rate limiting and retries.
        """
        # Cache check (GET only)
        if method.upper() == "GET":
            # Simple cache key: URL + stringified params
            params = kwargs.get("params", {})
            param_key = sorted(params.items()) if params else ""
            cache_key = f"{method}:{url}:{region_or_platform}:{param_key}"
            
            cached = await self.cache.get(cache_key)
            if cached:
                status, headers, content = cached
                return httpx.Response(status_code=status, headers=headers, content=content)

        # Hook: onRequest
        if "request" in self.hooks:
            await self.hooks["request"](method, url, kwargs)

        # 2. Execute with Retry
        response = await self._execute_with_retry(method, url, region_or_platform, **kwargs)

        # Hook: onResponse
        if "response" in self.hooks:
            await self.hooks["response"](response)
            
        # Cache set (only 200)
        if method.upper() == "GET" and response.status_code == 200:
             # Default TTL: 60s
             # Reconstruct cache_key to be safe or reuse if not modified
             params = kwargs.get("params", {})
             param_key = sorted(params.items()) if params else ""
             cache_key = f"{method}:{url}:{region_or_platform}:{param_key}"
             
             await self.cache.set(cache_key, (response.status_code, dict(response.headers), response.content), ttl=60)
            
        return response

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(3), # uses config in real usage
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException, httpx.RemoteProtocolError, ServerError)),
        reraise=True
    )
    async def _execute_with_retry(self, method: str, url: str, key: str, **kwargs: Any) -> httpx.Response:
        # TODO: Inject rate limit acquisition here once we have full method context.
        # For now, simplistic.
        
        # Construct full URL if needed
        if not url.startswith("https://"):
            # e.g. https://na1.api.riotgames.com/lol/summoner/v4/...
            host = f"https://{key}.api.riotgames.com"
            full_url = f"{host}{url}"
        else:
            full_url = url

        try:
            response = await self._client.request(method, full_url, **kwargs)
        except httpx.RequestError as e:
            logger.warning(f"Network error accessing {full_url}: {e}")
            raise

        # 3. Handle specific status codes
        if response.status_code == 429:
            retry_after = float(response.headers.get("Retry-After", "1"))
            logger.warning(f"Rate limited (429) on {key}. Wait {retry_after}s.")
            # If standard rate limit, we might want to sleep and retry internally or raise
            # Riot distinguishes between "App/Method Rate Limit" (headers) and "Service Rule" (429 w/o headers)
            # We raise so caller or outer loop decides, but typically we sleep.
            raise RateLimitError(response, retry_after)
        
        if response.status_code >= 500:
            logger.warning(f"Server error {response.status_code} on {key}")
            raise ServerError(response.status_code, "Server Error", response)
        
        if not response.is_success:
            # 400s, 401s, 403s, 404s
            raise RiotAPIError(response.status_code, response.text, response)

        # 4. Update Rate Limits
        # app_limits = response.headers.get("X-App-Rate-Limit")
        # app_counts = response.headers.get("X-App-Rate-Limit-Count")
        # await self.limiter.update(key, app_counts, app_limits)

        return response
