from importlib.metadata import PackageNotFoundError, version

from .auth import (
    RefreshingRsoTokenProvider,
    RsoClient,
    RsoConfig,
    RsoTokenProvider,
    StaticRsoTokenProvider,
    TokenResponse,
)
from .core.cache import AbstractCache, MemoryCache, NoOpCache
from .core.client import RiotClient
from .core.config import RiotClientConfig
from .core.http import (
    AuthMode,
    BadRequestError,
    ForbiddenError,
    MalformedResponseError,
    MissingCredentialError,
    NotFoundError,
    RateLimitError,
    ResponseValidationError,
    RiotAPIError,
    RiotNetworkError,
    RiotSkillIssueError,
    RiotTimeoutError,
    RiotTransportError,
    ServerError,
    UnauthorizedError,
)
from .core.pagination import paginate
from .core.ratelimit import AbstractRateLimiter, MemoryRateLimiter
from .core.sync_client import SyncRiotClient
from .core.types import (
    Game,
    PlatformRoute,
    RegionalRoute,
    RiotId,
    RouteKind,
    RouteResolutionError,
    ValorantRoute,
)
from .core.utils import gather_limited
from .services import MatchSummary, PlayerProfile
from .static import DataDragonClient, SyncDataDragonClient

try:
    __version__ = version("riotskillissue")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

try:
    from .core.cache import RedisCache
    from .core.ratelimit import RedisRateLimiter
except ImportError:
    pass

__all__ = [
    "AbstractCache",
    "AbstractRateLimiter",
    "AuthMode",
    "BadRequestError",
    "DataDragonClient",
    "ForbiddenError",
    "Game",
    "MalformedResponseError",
    "MatchSummary",
    "MemoryCache",
    "MemoryRateLimiter",
    "MissingCredentialError",
    "NoOpCache",
    "NotFoundError",
    "PlatformRoute",
    "PlayerProfile",
    "RateLimitError",
    "RefreshingRsoTokenProvider",
    "RegionalRoute",
    "ResponseValidationError",
    "RiotAPIError",
    "RiotClient",
    "RiotClientConfig",
    "RiotId",
    "RiotNetworkError",
    "RiotSkillIssueError",
    "RiotTimeoutError",
    "RiotTransportError",
    "RouteKind",
    "RouteResolutionError",
    "RsoClient",
    "RsoConfig",
    "RsoTokenProvider",
    "ServerError",
    "StaticRsoTokenProvider",
    "SyncDataDragonClient",
    "SyncRiotClient",
    "TokenResponse",
    "UnauthorizedError",
    "ValorantRoute",
    "__version__",
    "gather_limited",
    "paginate",
]
