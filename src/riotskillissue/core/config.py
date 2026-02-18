import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RiotClientConfig:
    """Immutable configuration for the Riot API client."""

    api_key: str
    redis_url: Optional[str] = None
    max_retries: int = 3
    connect_timeout: float = 5.0
    read_timeout: float = 10.0
    cache_ttl: int = 60
    """Default cache time-to-live in seconds for GET responses."""
    proxy: Optional[str] = None
    """Optional HTTP proxy URL (e.g. ``http://127.0.0.1:8080``)."""
    base_url: Optional[str] = None
    """Override the Riot API base URL (useful for testing)."""
    log_level: str = "WARNING"
    """Logging level for the library (DEBUG, INFO, WARNING)."""

    @classmethod
    def from_env(cls) -> "RiotClientConfig":
        """Create a config from environment variables."""
        return cls(
            api_key=os.environ.get("RIOT_API_KEY", ""),
            redis_url=os.environ.get("RIOT_REDIS_URL"),
            max_retries=int(os.environ.get("RIOT_MAX_RETRIES", "3")),
            cache_ttl=int(os.environ.get("RIOT_CACHE_TTL", "60")),
            proxy=os.environ.get("RIOT_PROXY"),
            base_url=os.environ.get("RIOT_BASE_URL"),
            log_level=os.environ.get("RIOT_LOG_LEVEL", "WARNING"),
        )
