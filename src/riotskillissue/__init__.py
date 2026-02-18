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
from .core.http import (
    RiotAPIError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

__all__ = [
    # Core
    "RiotClient",
    "SyncRiotClient",
    "RiotClientConfig",
    "__version__",
    # Enums
    "Region",
    "Platform",
    # Pagination
    "paginate",
    # Cache
    "AbstractCache",
    "MemoryCache",
    "NoOpCache",
    # Errors
    "RiotAPIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]
