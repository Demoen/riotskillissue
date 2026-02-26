"""riotskillissue – Production-ready, auto-updating Riot API wrapper."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("riotskillissue")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

from .core.client import RiotClient
from .core.sync_client import SyncRiotClient
from .core.config import RiotClientConfig
from .core.types import Region, Platform
from .core.pagination import paginate
from .core.cache import AbstractCache, MemoryCache, NoOpCache
from .core.ratelimit import AbstractRateLimiter, MemoryRateLimiter
from .core.utils import gather_limited
from .core.http import (
    RiotAPIError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from .static import DataDragonClient
from .auth import RsoClient, RsoConfig, TokenResponse

# Optional: RedisCache and RedisRateLimiter (require `pip install riotskillissue[redis]`)
try:
    from .core.cache import RedisCache
    from .core.ratelimit import RedisRateLimiter
except ImportError:
    pass

__all__ = [
    # Core
    "RiotClient",
    "SyncRiotClient",
    "RiotClientConfig",
    "__version__",
    # Enums
    "Region",
    "Platform",
    # Pagination & Utilities
    "paginate",
    "gather_limited",
    # Cache
    "AbstractCache",
    "MemoryCache",
    "NoOpCache",
    # Rate Limiting
    "AbstractRateLimiter",
    "MemoryRateLimiter",
    # Static Data
    "DataDragonClient",
    # Auth
    "RsoClient",
    "RsoConfig",
    "TokenResponse",
    # Errors
    "RiotAPIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]
