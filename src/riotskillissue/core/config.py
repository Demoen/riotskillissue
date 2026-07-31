from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from riotskillissue.core.types import (
    PlatformRoute,
    RegionalRoute,
    Route,
    ValorantRoute,
)

if TYPE_CHECKING:
    from riotskillissue.auth import RsoTokenProvider


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return default if value is None else int(value)


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    return default if value is None else float(value)


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean")


def _parse_default_route(value: Optional[object]) -> Optional[Route]:
    if value is None or value == "":
        return None
    if isinstance(value, (PlatformRoute, RegionalRoute, ValorantRoute)):
        return value
    if not isinstance(value, str):
        raise ValueError("default_route must be a route enum or string")
    normalized = value.strip().lower()
    for enum_type in (PlatformRoute, RegionalRoute, ValorantRoute):
        try:
            return enum_type(normalized)
        except ValueError:
            continue
    raise ValueError(f"unknown default route: {value}")


@dataclass(frozen=True)
class RiotClientConfig:
    api_key: str = field(default="", repr=False)
    default_route: Optional[Route] = None
    rso_token_provider: Optional["RsoTokenProvider"] = field(
        default=None, repr=False, compare=False
    )
    redis_url: Optional[str] = None
    max_retries: int = 3
    max_rate_limit_retries: int = 3
    connect_timeout: float = 5.0
    read_timeout: float = 10.0
    write_timeout: float = 10.0
    pool_timeout: float = 5.0
    max_retry_after: float = 120.0
    retry_backoff_base: float = 0.5
    retry_backoff_max: float = 10.0
    cache_ttl: int = 60
    cache_rso_responses: bool = False
    proxy: Optional[str] = None
    base_url: Optional[str] = None
    log_level: str = "WARNING"

    def __post_init__(self) -> None:
        key = self.api_key.strip() if isinstance(self.api_key, str) else ""
        object.__setattr__(self, "api_key", key)
        object.__setattr__(self, "default_route", _parse_default_route(self.default_route))

        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if self.max_rate_limit_retries < 0:
            raise ValueError("max_rate_limit_retries cannot be negative")
        if self.cache_ttl < 0:
            raise ValueError("cache_ttl cannot be negative")
        for name in (
            "connect_timeout",
            "read_timeout",
            "write_timeout",
            "pool_timeout",
            "max_retry_after",
            "retry_backoff_base",
            "retry_backoff_max",
        ):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be greater than zero")

    @classmethod
    def from_env(cls) -> "RiotClientConfig":
        token_provider = None
        rso_token = os.environ.get("RIOT_RSO_ACCESS_TOKEN", "").strip()
        if rso_token:
            from riotskillissue.auth import StaticRsoTokenProvider

            token_provider = StaticRsoTokenProvider(rso_token)

        return cls(
            api_key=os.environ.get("RIOT_API_KEY", ""),
            default_route=_parse_default_route(os.environ.get("RIOT_DEFAULT_ROUTE")),
            rso_token_provider=token_provider,
            redis_url=os.environ.get("RIOT_REDIS_URL"),
            max_retries=_env_int("RIOT_MAX_RETRIES", 3),
            max_rate_limit_retries=_env_int("RIOT_MAX_RATE_LIMIT_RETRIES", 3),
            connect_timeout=_env_float("RIOT_CONNECT_TIMEOUT", 5.0),
            read_timeout=_env_float("RIOT_READ_TIMEOUT", 10.0),
            write_timeout=_env_float("RIOT_WRITE_TIMEOUT", 10.0),
            pool_timeout=_env_float("RIOT_POOL_TIMEOUT", 5.0),
            max_retry_after=_env_float("RIOT_MAX_RETRY_AFTER", 120.0),
            retry_backoff_base=_env_float("RIOT_RETRY_BACKOFF_BASE", 0.5),
            retry_backoff_max=_env_float("RIOT_RETRY_BACKOFF_MAX", 10.0),
            cache_ttl=_env_int("RIOT_CACHE_TTL", 60),
            cache_rso_responses=_env_bool("RIOT_CACHE_RSO_RESPONSES", False),
            proxy=os.environ.get("RIOT_PROXY"),
            base_url=os.environ.get("RIOT_BASE_URL"),
            log_level=os.environ.get("RIOT_LOG_LEVEL", "WARNING"),
        )
