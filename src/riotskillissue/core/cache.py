from __future__ import annotations

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Optional, Any
import time
import asyncio


class AbstractCache(ABC):
    """Base cache interface."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int) -> None:
        pass

    async def delete(self, key: str) -> None:
        """Remove a single key (default no-op for backwards compat)."""
        pass

    async def clear(self) -> None:
        """Remove all entries (default no-op for backwards compat)."""
        pass


class MemoryCache(AbstractCache):
    """In-process LRU cache with TTL support.

    Args:
        max_size: Maximum number of entries. 0 means unbounded.
    """

    def __init__(self, max_size: int = 1024):
        self._store: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._lock = asyncio.Lock()
        self.max_size = max_size

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._store:
                val, expire_at = self._store[key]
                if time.time() < expire_at:
                    # Move to end (most-recently used)
                    self._store.move_to_end(key)
                    return val
                else:
                    del self._store[key]
        return None

    async def set(self, key: str, value: Any, ttl: int) -> None:
        async with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = (value, time.time() + ttl)
            # Evict oldest entries if over capacity
            if self.max_size > 0:
                while len(self._store) > self.max_size:
                    self._store.popitem(last=False)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._store.clear()


class NoOpCache(AbstractCache):
    async def get(self, key: str) -> Optional[Any]:
        return None

    async def set(self, key: str, value: Any, ttl: int) -> None:
        pass


try:
    from redis.asyncio import Redis
    import pickle

    class RedisCache(AbstractCache):
        def __init__(self, redis_url: str):
            self.redis = Redis.from_url(redis_url)

        async def get(self, key: str) -> Optional[Any]:
            val = await self.redis.get(key)
            if val:
                return pickle.loads(val)  # noqa: S301
            return None

        async def set(self, key: str, value: Any, ttl: int) -> None:
            val = pickle.dumps(value)
            await self.redis.set(key, val, ex=ttl)

        async def delete(self, key: str) -> None:
            await self.redis.delete(key)

        async def clear(self) -> None:
            # Only clear keys with our prefix would be safer, but for now
            # we flush the entire namespace.
            await self.redis.flushdb()

except ImportError:
    pass
