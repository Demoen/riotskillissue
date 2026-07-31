from __future__ import annotations

import logging
from dataclasses import replace
from types import TracebackType
from typing import TYPE_CHECKING, Any

from riotskillissue.api.client_mixin import GeneratedClientMixin
from riotskillissue.core.cache import AbstractCache
from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.http import HttpClient, MissingCredentialError
from riotskillissue.core.types import Route
from riotskillissue.services import (
    LolService,
    LorService,
    RiftboundService,
    TftService,
    ValorantService,
)
from riotskillissue.static import DataDragonClient

if TYPE_CHECKING:
    from riotskillissue.auth import RsoTokenProvider


class RiotClient(GeneratedClientMixin):
    def __init__(
        self,
        api_key: str | None = None,
        config: RiotClientConfig | None = None,
        cache: AbstractCache | None = None,
        hooks: dict[str, Any] | None = None,
        *,
        default_route: Route | str | None = None,
        rso_token_provider: RsoTokenProvider | None = None,
    ) -> None:
        if api_key is not None and not api_key.strip():
            raise MissingCredentialError("api_key")

        resolved = config or RiotClientConfig.from_env()
        overrides: dict[str, Any] = {}
        if api_key is not None:
            overrides["api_key"] = api_key
        if default_route is not None:
            overrides["default_route"] = default_route
        if rso_token_provider is not None:
            overrides["rso_token_provider"] = rso_token_provider
        if overrides:
            resolved = replace(resolved, **overrides)

        self.config = resolved
        self.http = HttpClient(resolved, cache=cache, hooks=hooks)
        self._static = DataDragonClient(cache=cache)
        super().__init__(self.http)

        self.lol = LolService(self.raw, self._static)
        self.tft = TftService(self.raw)
        self.valorant = ValorantService(self.raw)
        self.lor = LorService(self.raw)
        self.riftbound = RiftboundService(self.raw)

        logging.getLogger("riotskillissue").setLevel(
            getattr(logging, resolved.log_level.upper(), logging.WARNING)
        )

    @property
    def static(self) -> DataDragonClient:
        return self._static

    async def call_operation(
        self,
        operation: str,
        arguments: dict[str, Any],
    ) -> Any:
        return await self.raw.call_operation(operation, arguments)

    async def close(self) -> None:
        await self.http.close()
        await self._static.close()

    async def __aenter__(self) -> RiotClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"<RiotClient default_route={self.config.default_route!r}>"
