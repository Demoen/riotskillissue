from abc import ABC, abstractmethod
from typing import Optional, Any
import time
import asyncio

class AbstractCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int) -> None:
        pass

class MemoryCache(AbstractCache):
    def __init__(self):
        self._store = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._store:
                val, expire_at = self._store[key]
                if time.time() < expire_at:
                    return val
                else:
                    del self._store[key]
        return None

    async def set(self, key: str, value: Any, ttl: int) -> None:
        async with self._lock:
            self._store[key] = (value, time.time() + ttl)

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
                return pickle.loads(val)
            return None

        async def set(self, key: str, value: Any, ttl: int) -> None:
            val = pickle.dumps(value)
            await self.redis.set(key, val, ex=ttl)
			
except ImportError:
    pass
