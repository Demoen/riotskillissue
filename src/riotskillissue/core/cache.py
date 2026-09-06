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
    import json as _json
    import base64 as _base64

    class RedisCache(AbstractCache):
        _prefix = "riot:cache:"

        def __init__(self, redis_url: str):
            self.redis = Redis.from_url(redis_url)

        async def get(self, key: str) -> Optional[Any]:
            val = await self.redis.get(f"{self._prefix}{key}")
            if val:
                return _deserialize(_json.loads(val))
            return None

        async def set(self, key: str, value: Any, ttl: int) -> None:
            val = _json.dumps(_serialize(value))
            await self.redis.set(f"{self._prefix}{key}", val, ex=ttl)

        async def delete(self, key: str) -> None:
            await self.redis.delete(f"{self._prefix}{key}")

        async def clear(self) -> None:
            keys = []
            async for key in self.redis.scan_iter(match=f"{self._prefix}*", count=100):
                keys.append(key)
                if len(keys) >= 100:
                    await self.redis.delete(*keys)
                    keys.clear()
            if keys:
                await self.redis.delete(*keys)

    def _serialize(obj: Any) -> Any:
        """Convert an object to a JSON-safe representation."""
        if isinstance(obj, bytes):
            return {"__bytes__": _base64.b64encode(obj).decode("ascii")}
        if isinstance(obj, tuple):
            return {"__tuple__": [_serialize(item) for item in obj]}
        if isinstance(obj, list):
            return [_serialize(item) for item in obj]
        if isinstance(obj, dict):
            return {"__dict__": [[_serialize(k), _serialize(v)] for k, v in obj.items()]}
        return obj

    def _deserialize(obj: Any) -> Any:
        """Restore an object from its JSON-safe representation."""
        if isinstance(obj, dict):
            if "__dict__" in obj:
                return {_deserialize(k): _deserialize(v) for k, v in obj["__dict__"]}
            if "__bytes__" in obj:
                return _base64.b64decode(obj["__bytes__"])
            if "__tuple__" in obj:
                return tuple(_deserialize(item) for item in obj["__tuple__"])
            return {k: _deserialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_deserialize(item) for item in obj]
        return obj

except ImportError:
    pass
