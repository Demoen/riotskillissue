import logging
from typing import Optional, Type
from types import TracebackType

from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.http import HttpClient
from riotskillissue.api.client_mixin import GeneratedClientMixin
from riotskillissue.core.cache import AbstractCache

logger = logging.getLogger(__name__)


class RiotClient(GeneratedClientMixin):
    """Main entry point for the Riot Games API.

    Usage::

        async with RiotClient(api_key="RGAPI-...") as client:
            summoner = await client.summoner.get_by_puuid(
                region="na1", encrypted_puuid="..."
            )
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[RiotClientConfig] = None,
        cache: Optional[AbstractCache] = None,
        hooks: Optional[dict] = None,
    ):
        if config is None:
            if api_key:
                config = RiotClientConfig(api_key=api_key)
            else:
                config = RiotClientConfig.from_env()

        self.config = config
        self._cache = cache
        self.http = HttpClient(config, cache=cache, hooks=hooks)

        # Configure library-wide logging level
        logging.getLogger("riotskillissue").setLevel(
            getattr(logging, config.log_level.upper(), logging.WARNING)
        )

        # Lazy-initialised static data client (created on first access)
        self._static: Optional["DataDragonClient"] = None  # type: ignore[name-defined]

        # Initialize generated APIs
        super().__init__(self.http)

    # -- Lazy Data Dragon access ---------------------------------------------

    @property
    def static(self) -> "DataDragonClient":  # type: ignore[name-defined]
        """Data Dragon client (created lazily on first access)."""
        if self._static is None:
            from riotskillissue.static import DataDragonClient

            self._static = DataDragonClient(cache=self._cache)
        return self._static

    # -- Lifecycle -----------------------------------------------------------

    async def close(self) -> None:
        """Close underlying HTTP connections.

        Prefer using the client as an async context manager instead.
        """
        await self.http.close()
        if self._static is not None:
            await self._static.close()

    async def __aenter__(self) -> "RiotClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    def __repr__(self) -> str:
        masked = self.config.api_key[:8] + "..." if len(self.config.api_key) > 8 else "***"
        return f"<RiotClient key={masked}>"
