from __future__ import annotations

import asyncio
import threading
from collections.abc import Awaitable
from types import TracebackType
from typing import TYPE_CHECKING, Any, TypeVar

from riotskillissue.api.raw import SyncGeneratedRawClient
from riotskillissue.core.cache import AbstractCache
from riotskillissue.core.client import RiotClient
from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.types import Route
from riotskillissue.services import (
    SyncLolService,
    SyncLorService,
    SyncRiftboundService,
    SyncTftService,
    SyncValorantService,
)
from riotskillissue.static import SyncDataDragonClient

if TYPE_CHECKING:
    from riotskillissue.auth import RsoTokenProvider

T = TypeVar("T")


class _LoopThread:
    def __init__(self) -> None:
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._loop is not None:
            return
        ready = threading.Event()

        def run() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            ready.set()
            loop.run_forever()

        self._thread = threading.Thread(
            target=run,
            daemon=True,
            name="riotskillissue-sync",
        )
        self._thread.start()
        ready.wait()

    def run(self, awaitable: Awaitable[T]) -> T:
        if self._loop is None:
            raise RuntimeError("Synchronous client is closed")

        async def consume() -> T:
            return await awaitable

        return asyncio.run_coroutine_threadsafe(consume(), self._loop).result()

    def stop(self) -> None:
        loop = self._loop
        thread = self._thread
        if loop is None:
            return
        loop.call_soon_threadsafe(loop.stop)
        if thread is not None:
            thread.join(timeout=5)
        loop.close()
        self._loop = None
        self._thread = None


class SyncRiotClient:
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
        self._loop_thread = _LoopThread()
        self._loop_thread.start()
        try:
            self._async_client = RiotClient(
                api_key=api_key,
                config=config,
                cache=cache,
                hooks=hooks,
                default_route=default_route,
                rso_token_provider=rso_token_provider,
            )
        except BaseException:
            self._loop_thread.stop()
            raise

        self.config = self._async_client.config
        self.raw = SyncGeneratedRawClient(self._async_client.raw, self._run)
        self.static = SyncDataDragonClient(self._async_client.static, self._run)
        self.lol = SyncLolService(self._async_client.lol, self._run, self.static)
        self.tft = SyncTftService(self._async_client.tft, self._run)
        self.valorant = SyncValorantService(self._async_client.valorant, self._run)
        self.lor = SyncLorService(self._async_client.lor, self._run)
        self.riftbound = SyncRiftboundService(
            self._async_client.riftbound,
            self._run,
        )

    def _run(self, awaitable: Awaitable[T]) -> T:
        return self._loop_thread.run(awaitable)

    def call_operation(
        self,
        operation: str,
        arguments: dict[str, Any],
    ) -> Any:
        return self.raw.call_operation(operation, arguments)

    def close(self) -> None:
        self._run(self._async_client.close())
        self._loop_thread.stop()

    def __enter__(self) -> SyncRiotClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<SyncRiotClient default_route={self.config.default_route!r}>"
