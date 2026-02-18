"""Synchronous wrapper around the async ``RiotClient``.

Usage::

    from riotskillissue import SyncRiotClient

    with SyncRiotClient(api_key="RGAPI-...") as client:
        summoner = client.summoner.get_by_puuid(region="na1", encrypted_puuid="...")
        print(summoner)

Internally a dedicated event loop runs on a background daemon thread, so
it is safe to use ``SyncRiotClient`` from synchronous code even when an
event loop is already running (e.g. inside Jupyter notebooks).
"""

from __future__ import annotations

import asyncio
import functools
import threading
from types import TracebackType
from typing import Any, Callable, Coroutine, Optional, Type, TypeVar

from riotskillissue.core.client import RiotClient
from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.cache import AbstractCache

T = TypeVar("T")


class _LoopThread:
    """Manages a background thread running an asyncio event loop."""

    def __init__(self) -> None:
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> asyncio.AbstractEventLoop:
        if self._loop is not None:
            return self._loop
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, daemon=True, name="riotskillissue-sync"
        )
        self._thread.start()
        return self._loop

    def run(self, coro: Coroutine[Any, Any, T]) -> T:
        assert self._loop is not None, "Loop not started"
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def stop(self) -> None:
        if self._loop is not None:
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread is not None:
                self._thread.join(timeout=5)
            self._loop.close()
            self._loop = None
            self._thread = None


class _SyncProxy:
    """Wraps an async endpoint API, turning every async method into a sync call."""

    def __init__(self, async_api: Any, runner: Callable[..., Any]) -> None:
        self._api = async_api
        self._run = runner

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._api, name)
        if asyncio.iscoroutinefunction(attr):

            @functools.wraps(attr)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return self._run(attr(*args, **kwargs))

            return wrapper
        return attr


class SyncRiotClient:
    """Synchronous Riot API client.

    Mirrors the full API surface of :class:`~riotskillissue.core.client.RiotClient`
    but all endpoint methods block instead of returning coroutines.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[RiotClientConfig] = None,
        cache: Optional[AbstractCache] = None,
        hooks: Optional[dict] = None,
    ):
        self._loop_thread = _LoopThread()
        self._loop_thread.start()

        self._async_client = RiotClient(
            api_key=api_key, config=config, cache=cache, hooks=hooks
        )

        # Create synchronous proxy for every generated API accessor
        self.config = self._async_client.config

        # Dynamically mirror all endpoint accessors
        self._proxy_cache: dict[str, _SyncProxy] = {}

    def _run(self, coro: Coroutine[Any, Any, T]) -> T:
        return self._loop_thread.run(coro)

    def __getattr__(self, name: str) -> Any:
        # Proxy attribute access to the underlying async client and wrap
        if name.startswith("_"):
            raise AttributeError(name)

        if name in self._proxy_cache:
            return self._proxy_cache[name]

        attr = getattr(self._async_client, name)
        if hasattr(attr, "__self__") or hasattr(attr, "http"):
            # It's an API namespace (e.g. client.summoner)
            proxy = _SyncProxy(attr, self._run)
            self._proxy_cache[name] = proxy
            return proxy
        return attr

    @property
    def static(self) -> _SyncProxy:
        """Synchronous Data Dragon proxy."""
        if "static" not in self._proxy_cache:
            self._proxy_cache["static"] = _SyncProxy(
                self._async_client.static, self._run
            )
        return self._proxy_cache["static"]

    def close(self) -> None:
        """Close all connections and stop the background loop."""
        self._run(self._async_client.close())
        self._loop_thread.stop()

    def __enter__(self) -> "SyncRiotClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<SyncRiotClient wrapping {self._async_client!r}>"
