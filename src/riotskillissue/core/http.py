from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import math
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from enum import Enum
from typing import Any, Callable, Iterable, Optional, Sequence, Union
from urllib.parse import urlparse

import httpx
from pydantic import TypeAdapter, ValidationError

from riotskillissue.core.cache import AbstractCache, NoOpCache
from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.ratelimit import (
    AbstractRateLimiter,
    MemoryRateLimiter,
    RedisRateLimiter,
    parse_rate_limits,
)
from riotskillissue.core.types import (
    PlatformRoute,
    RegionalRoute,
    Route,
    RouteKind,
    RouteResolutionError,
    ValorantRoute,
    resolve_route,
)

logger = logging.getLogger(__name__)

_UNSET = object()
_SENSITIVE_HEADERS = {"authorization", "x-riot-token"}
_IDEMPOTENT_METHODS = {"GET", "HEAD", "OPTIONS", "PUT", "DELETE", "TRACE"}


class RiotSkillIssueError(Exception):
    pass


class MissingCredentialError(RiotSkillIssueError):
    def __init__(self, auth_mode: str) -> None:
        self.auth_mode = auth_mode
        super().__init__(f"credential required for auth mode {auth_mode}")


class RiotTransportError(RiotSkillIssueError):
    pass


class RiotNetworkError(RiotTransportError):
    pass


class RiotTimeoutError(RiotTransportError):
    pass


class MalformedResponseError(RiotSkillIssueError):
    def __init__(
        self,
        message: str = "Riot API returned malformed JSON",
        *,
        response: Optional[httpx.Response] = None,
    ) -> None:
        self.response = response
        super().__init__(message)


class ResponseValidationError(RiotSkillIssueError):
    def __init__(
        self,
        message: str = "Riot API response failed validation",
        *,
        response: Optional[httpx.Response] = None,
        operation_id: Optional[str] = None,
    ) -> None:
        self.response = response
        self.operation_id = operation_id
        super().__init__(message)


class RiotAPIError(RiotSkillIssueError):
    def __init__(
        self,
        status: int,
        message: str,
        response: Optional[httpx.Response] = None,
    ) -> None:
        self.status = status
        self.message = message
        self.response = response
        super().__init__(f"[{status}] {message}")


class BadRequestError(RiotAPIError):
    def __init__(self, response: httpx.Response):
        super().__init__(400, "Bad Request", response)


class UnauthorizedError(RiotAPIError):
    def __init__(self, response: httpx.Response):
        super().__init__(401, "Unauthorized", response)


class ForbiddenError(RiotAPIError):
    def __init__(self, response: httpx.Response):
        super().__init__(403, "Forbidden", response)


class NotFoundError(RiotAPIError):
    def __init__(self, response: httpx.Response):
        super().__init__(404, "Not Found", response)


class RateLimitError(RiotAPIError):
    def __init__(
        self,
        response: httpx.Response,
        retry_after: float,
        *,
        retries: int = 0,
    ) -> None:
        super().__init__(429, f"Rate limited; retry after {retry_after:g}s", response)
        self.retry_after = retry_after
        self.retries = retries


class ServerError(RiotAPIError):
    def __init__(self, response: httpx.Response):
        super().__init__(response.status_code, "Server Error", response)


class AuthMode(str, Enum):
    API_KEY = "api_key"
    RSO = "rso"
    NONE = "none"


NetworkError = RiotNetworkError
RequestTimeoutError = RiotTimeoutError

_STATUS_ERROR_MAP = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
}


def _normalize_auth_mode(value: Union[AuthMode, str, Enum, None]) -> AuthMode:
    if value is None:
        return AuthMode.API_KEY
    if isinstance(value, AuthMode):
        return value
    raw = value.value if isinstance(value, Enum) else value
    normalized = str(raw).strip().lower().replace("-", "_")
    if normalized in {
        "api",
        "apikey",
        "api_key",
        "riot_token",
        "x_riot_token",
    }:
        return AuthMode.API_KEY
    if normalized in {"rso", "bearer", "oauth", "oauth2"}:
        return AuthMode.RSO
    if normalized in {"none", "public", "unauthenticated"}:
        return AuthMode.NONE
    raise ValueError(f"unknown auth mode: {raw}")


def _route_value(route: object) -> str:
    value = route.value if isinstance(route, Enum) else route
    if not isinstance(value, str):
        raise RouteResolutionError("unknown", explicit=route)
    normalized = value.strip().lower()
    valid = {
        member.value
        for enum_type in (PlatformRoute, RegionalRoute, ValorantRoute)
        for member in enum_type
    }
    if normalized not in valid:
        raise RouteResolutionError("unknown", explicit=route)
    return normalized


class HttpClient:
    def __init__(
        self,
        config: RiotClientConfig,
        rate_limiter: Optional[AbstractRateLimiter] = None,
        cache: Optional[AbstractCache] = None,
        hooks: Optional[dict[str, Callable[..., Any]]] = None,
        rso_token_provider: Optional[object] = None,
    ) -> None:
        self.config = config
        self.cache = cache or NoOpCache()
        self.hooks = hooks or {}
        self._rso_token_provider = (
            rso_token_provider
            if rso_token_provider is not None
            else config.rso_token_provider
        )
        self._client = httpx.AsyncClient(
            headers={"Accept-Encoding": "identity"},
            timeout=httpx.Timeout(
                connect=config.connect_timeout,
                read=config.read_timeout,
                write=config.write_timeout,
                pool=config.pool_timeout,
            ),
            proxy=config.proxy,
        )

        self._owns_limiter = rate_limiter is None
        if rate_limiter is not None:
            self.limiter = rate_limiter
        elif config.redis_url:
            self.limiter = RedisRateLimiter(config.redis_url)
        else:
            self.limiter = MemoryRateLimiter()

        self._default_app_limits = parse_rate_limits("20:1,100:120")
        self._app_limits: dict[str, list[Any]] = {}
        self._method_limits: dict[str, list[Any]] = {}

    async def close(self) -> None:
        try:
            await self._client.aclose()
        finally:
            if self._owns_limiter:
                await self.limiter.close()

    def resolve_route(
        self,
        route_kind: Union[RouteKind, str],
        explicit: Optional[object] = None,
        *,
        allowed_routes: Optional[Sequence[str]] = None,
    ) -> Route:
        resolved = resolve_route(
            route_kind,
            explicit=explicit,
            default=self.config.default_route,
        )
        if allowed_routes is not None:
            allowed = {
                route.value if isinstance(route, Enum) else str(route).lower()
                for route in allowed_routes
            }
            if (
                explicit is None
                and resolved is RegionalRoute.ASIA
                and RegionalRoute.APAC.value in allowed
                and RegionalRoute.ASIA.value not in allowed
            ):
                resolved = RegionalRoute.APAC
            if resolved.value not in allowed:
                raise RouteResolutionError(
                    route_kind,
                    explicit=explicit,
                    default=self.config.default_route,
                    reason=f"route {resolved.value} is not allowed for this operation",
                )
        return resolved

    async def request(
        self,
        method: str,
        url: str,
        region_or_platform: Optional[object] = None,
        *,
        route_kind: Optional[Union[RouteKind, str]] = None,
        route: Optional[object] = None,
        allowed_routes: Optional[Sequence[str]] = None,
        operation_id: Optional[str] = None,
        auth_mode: Union[AuthMode, str, Enum, None] = AuthMode.API_KEY,
        cache_user_scoped: bool = False,
        cache: Optional[bool] = None,
        response_adapter: Any = _UNSET,
        response_type: Any = _UNSET,
        successful_statuses: Optional[Iterable[int]] = None,
        no_content_statuses: Optional[Iterable[int]] = None,
        **kwargs: Any,
    ) -> Any:
        if response_adapter is not _UNSET and response_type is not _UNSET:
            raise TypeError("pass only one of response_adapter and response_type")
        adapter = (
            response_adapter if response_adapter is not _UNSET else response_type
        )
        parse_response = adapter is not _UNSET

        explicit_route = region_or_platform if region_or_platform is not None else route
        if route_kind is not None:
            resolved = self.resolve_route(
                route_kind,
                explicit_route,
                allowed_routes=allowed_routes,
            )
            route_name = resolved.value
        elif explicit_route is not None:
            route_name = _route_value(explicit_route)
            if allowed_routes is not None and route_name not in {
                str(item.value if isinstance(item, Enum) else item).lower()
                for item in allowed_routes
            }:
                raise RouteResolutionError(
                    "unknown",
                    explicit=explicit_route,
                    reason=f"route {route_name} is not allowed for this operation",
                )
        else:
            raise RouteResolutionError(
                route_kind or "unknown",
                default=self.config.default_route,
                reason="a route kind or explicit route is required",
            )

        normalized_method = method.upper()
        mode, auth_headers, auth_scope = await self._resolve_auth(auth_mode)
        request_kwargs = dict(kwargs)
        request_kwargs["headers"] = self._merge_headers(
            request_kwargs.get("headers"), auth_headers
        )
        full_url = self._build_url(url, route_name)

        use_cache = normalized_method == "GET" and self.config.cache_ttl > 0
        if cache is not None:
            use_cache = use_cache and cache
        if mode is AuthMode.RSO and cache is None:
            use_cache = use_cache and self.config.cache_rso_responses
        if cache_user_scoped and mode is AuthMode.NONE:
            use_cache = False

        cache_key: Optional[str] = None
        if use_cache:
            cache_key = self._cache_key(
                normalized_method,
                url,
                route_name,
                request_kwargs,
                auth_scope=auth_scope,
                operation_id=operation_id,
            )
            cached = await self.cache.get(cache_key)
            if cached is not None:
                status, headers, content = cached
                response = httpx.Response(
                    status_code=status,
                    headers=headers,
                    content=content,
                    request=httpx.Request(normalized_method, full_url),
                )
                if parse_response:
                    return self._adapt_response(
                        response,
                        adapter,
                        operation_id=operation_id,
                        no_content_statuses=no_content_statuses,
                    )
                return response

        request_hook = self.hooks.get("request")
        if request_hook is not None:
            await request_hook(
                normalized_method,
                url,
                self._sanitize_hook_kwargs(request_kwargs),
            )

        response = await self._execute_with_retry(
            normalized_method,
            url,
            route_name,
            operation_id=operation_id,
            auth_scope=auth_scope,
            successful_statuses=successful_statuses,
            **request_kwargs,
        )

        response_hook = self.hooks.get("response")
        if response_hook is not None:
            await response_hook(response)

        result: Any = response
        if parse_response:
            result = self._adapt_response(
                response,
                adapter,
                operation_id=operation_id,
                no_content_statuses=no_content_statuses,
            )

        if use_cache and response.is_success:
            if cache_key is None:
                cache_key = self._cache_key(
                    normalized_method,
                    url,
                    route_name,
                    request_kwargs,
                    auth_scope=auth_scope,
                    operation_id=operation_id,
                )
            await self.cache.set(
                cache_key,
                (response.status_code, dict(response.headers), response.content),
                ttl=self.config.cache_ttl,
            )

        return result

    async def _resolve_auth(
        self, auth_mode: Union[AuthMode, str, Enum, None]
    ) -> tuple[AuthMode, dict[str, str], str]:
        mode = _normalize_auth_mode(auth_mode)
        if mode is AuthMode.NONE:
            return mode, {}, "none"
        if mode is AuthMode.API_KEY:
            api_key = self.config.api_key.strip()
            if not api_key:
                raise MissingCredentialError(mode.value)
            return (
                mode,
                {"X-Riot-Token": api_key},
                f"api_key:{self._credential_fingerprint(api_key)}",
            )

        provider = self._rso_token_provider
        if provider is None:
            raise MissingCredentialError(mode.value)
        getter = getattr(provider, "get_token", None)
        if getter is None:
            getter = getattr(provider, "get_access_token", None)
        if getter is None:
            raise MissingCredentialError(mode.value)
        token = await getter()
        if not isinstance(token, str) or not token.strip():
            raise MissingCredentialError(mode.value)
        token = token.strip()
        return (
            mode,
            {"Authorization": f"Bearer {token}"},
            f"rso:{self._credential_fingerprint(token)}",
        )

    @staticmethod
    def _credential_fingerprint(credential: str) -> str:
        return hashlib.sha256(credential.encode("utf-8")).hexdigest()

    @staticmethod
    def _merge_headers(
        headers: Any, auth_headers: dict[str, str]
    ) -> httpx.Headers:
        merged = httpx.Headers(headers)
        for name in tuple(merged.keys()):
            if name.lower() in _SENSITIVE_HEADERS:
                del merged[name]
        for name, value in auth_headers.items():
            merged[name] = value
        if "Accept-Encoding" not in merged:
            merged["Accept-Encoding"] = "identity"
        return merged

    @staticmethod
    def _sanitize_hook_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
        sanitized = dict(kwargs)
        headers = httpx.Headers(sanitized.get("headers"))
        for name in tuple(headers.keys()):
            if name.lower() in _SENSITIVE_HEADERS:
                del headers[name]
        sanitized["headers"] = headers
        return sanitized

    @staticmethod
    def _cache_key(
        method: str,
        url: str,
        region: object,
        kwargs: dict[str, Any],
        *,
        auth_scope: str = "none",
        operation_id: Optional[str] = None,
    ) -> str:
        material = {
            "method": method.upper(),
            "url": url,
            "route": _route_value(region),
            "operation": operation_id,
            "params": kwargs.get("params"),
            "json": kwargs.get("json"),
            "auth_scope": auth_scope,
        }
        encoded = json.dumps(
            material,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return f"riot:v1:{hashlib.sha256(encoded).hexdigest()}"

    def _build_url(self, url: str, route: str) -> str:
        if url.startswith(("http://", "https://")):
            parsed = urlparse(url)
            expected_base = self.config.base_url
            if expected_base:
                expected = urlparse(expected_base)
                if (parsed.scheme, parsed.netloc) != (expected.scheme, expected.netloc):
                    raise ValueError("absolute URL does not match configured base_url")
            elif parsed.scheme != "https" or parsed.hostname != (
                f"{route}.api.riotgames.com"
            ):
                raise ValueError("absolute URL is outside the selected Riot route")
            return url
        path = url if url.startswith("/") else f"/{url}"
        host = (
            self.config.base_url.rstrip("/")
            if self.config.base_url
            else f"https://{route}.api.riotgames.com"
        )
        return f"{host}{path}"

    async def _execute_with_retry(
        self,
        method: str,
        url: str,
        key: object,
        *,
        operation_id: Optional[str] = None,
        auth_scope: str = "none",
        successful_statuses: Optional[Iterable[int]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        route = _route_value(key)
        full_url = self._build_url(url, route)
        operation_scope = operation_id or hashlib.sha256(
            f"{method}:{urlparse(full_url).path}".encode()
        ).hexdigest()
        rate_auth_scope = "rso" if auth_scope.startswith("rso:") else auth_scope
        app_key = f"app:{route}:{rate_auth_scope}"
        method_key = f"method:{route}:{rate_auth_scope}:{operation_scope}"
        can_replay = method.upper() in _IDEMPOTENT_METHODS
        transient_retries = 0
        rate_limit_retries = 0
        expected_statuses = (
            {int(status) for status in successful_statuses}
            if successful_statuses is not None
            else None
        )

        while True:
            app_limits = self._app_limits.get(app_key, self._default_app_limits)
            await self.limiter.acquire(app_key, app_limits)
            method_limits = self._method_limits.get(method_key, [])
            if method_limits:
                await self.limiter.acquire(method_key, method_limits)

            try:
                response = await self._client.request(method, full_url, **kwargs)
            except httpx.TimeoutException as exc:
                safe_to_retry = can_replay or isinstance(
                    exc, (httpx.ConnectTimeout, httpx.PoolTimeout)
                )
                if not safe_to_retry or transient_retries >= self.config.max_retries:
                    raise RiotTimeoutError("Riot API request timed out") from exc
                transient_retries += 1
                await asyncio.sleep(self._retry_delay(transient_retries))
                continue
            except (httpx.NetworkError, httpx.RemoteProtocolError) as exc:
                safe_to_retry = can_replay or isinstance(exc, httpx.ConnectError)
                if not safe_to_retry or transient_retries >= self.config.max_retries:
                    raise RiotNetworkError("Riot API network request failed") from exc
                transient_retries += 1
                await asyncio.sleep(self._retry_delay(transient_retries))
                continue
            except httpx.RequestError as exc:
                if not can_replay or transient_retries >= self.config.max_retries:
                    raise RiotNetworkError("Riot API request failed") from exc
                transient_retries += 1
                await asyncio.sleep(self._retry_delay(transient_retries))
                continue

            await self._update_rate_limits(response, app_key, method_key)

            if response.status_code == 429:
                retry_after = self._retry_after(response.headers.get("Retry-After"))
                if rate_limit_retries >= self.config.max_rate_limit_retries:
                    raise RateLimitError(
                        response,
                        retry_after,
                        retries=rate_limit_retries,
                    )
                rate_limit_retries += 1
                logger.warning(
                    "Rate limited for operation %s; retrying in %.2fs",
                    operation_id or "<unknown>",
                    retry_after,
                )
                await asyncio.sleep(retry_after)
                continue

            if response.status_code >= 500:
                if not can_replay or transient_retries >= self.config.max_retries:
                    raise ServerError(response)
                transient_retries += 1
                await asyncio.sleep(self._retry_delay(transient_retries))
                continue

            if not response.is_success:
                error_class = _STATUS_ERROR_MAP.get(response.status_code)
                if error_class is not None:
                    raise error_class(response)
                raise RiotAPIError(
                    response.status_code,
                    "Riot API request failed",
                    response,
                )

            if expected_statuses is not None and response.status_code not in expected_statuses:
                logger.debug(
                    "Operation %s returned undocumented success status %d",
                    operation_id or "<unknown>",
                    response.status_code,
                )
            return response

    async def _update_rate_limits(
        self,
        response: httpx.Response,
        app_key: str,
        method_key: str,
    ) -> None:
        app_limits_header = response.headers.get("X-App-Rate-Limit")
        app_counts = response.headers.get("X-App-Rate-Limit-Count")
        if app_limits_header:
            parsed = parse_rate_limits(app_limits_header)
            if parsed:
                self._app_limits[app_key] = parsed
        if app_counts:
            await self.limiter.update(app_key, app_counts, app_limits_header)

        method_limits_header = response.headers.get("X-Method-Rate-Limit")
        method_counts = response.headers.get("X-Method-Rate-Limit-Count")
        if method_limits_header:
            parsed = parse_rate_limits(method_limits_header)
            if parsed:
                self._method_limits[method_key] = parsed
        if method_counts:
            await self.limiter.update(
                method_key,
                method_counts,
                method_limits_header,
            )

    def _retry_delay(self, retry_number: int) -> float:
        delay = self.config.retry_backoff_base * (2 ** max(retry_number - 1, 0))
        return float(min(float(delay), self.config.retry_backoff_max))

    def _retry_after(self, value: Optional[str]) -> float:
        delay = 1.0
        if value:
            try:
                delay = float(value)
            except ValueError:
                try:
                    parsed = parsedate_to_datetime(value)
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    delay = (parsed - datetime.now(timezone.utc)).total_seconds()
                except (TypeError, ValueError, OverflowError):
                    delay = 1.0
        if not math.isfinite(delay) or delay < 0:
            delay = 1.0
        return min(delay, self.config.max_retry_after)

    @staticmethod
    def _adapt_response(
        response: httpx.Response,
        adapter: Any,
        *,
        operation_id: Optional[str],
        no_content_statuses: Optional[Iterable[int]],
    ) -> Any:
        empty_statuses = (
            {int(status) for status in no_content_statuses}
            if no_content_statuses is not None
            else set()
        )
        if response.status_code in empty_statuses or not response.content:
            payload: Any = None
        else:
            try:
                payload = response.json()
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
                raise MalformedResponseError(response=response) from exc

        if adapter is None:
            return payload
        try:
            if hasattr(adapter, "validate_python"):
                return adapter.validate_python(payload)
            if isinstance(adapter, type):
                return TypeAdapter(adapter).validate_python(payload)
            return adapter(payload)
        except (ValidationError, TypeError, ValueError) as exc:
            raise ResponseValidationError(
                response=response,
                operation_id=operation_id,
            ) from exc
