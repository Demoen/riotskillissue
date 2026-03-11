from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

try:
    import redis.asyncio as redis
except ImportError:
    redis = None  # type: ignore

logger = logging.getLogger(__name__)

class RateLimitBucket:
    """Represents a single rate limit bucket (e.g., 20 requests per 1 second)."""
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window

    def __repr__(self) -> str:
        return f"{self.limit}:{self.window}"

def parse_rate_limits(header_value: str) -> List[RateLimitBucket]:
    """Parses Riot limit headers like '20:1,100:120'."""
    if not header_value:
        return []
    buckets = []
    for part in header_value.split(','):
        try:
            limit, window = map(int, part.split(':'))
            buckets.append(RateLimitBucket(limit, window))
        except ValueError:
            pass
    return buckets

class AbstractRateLimiter(ABC):
    @abstractmethod
    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        """Wait until a request can be made."""
        pass

    @abstractmethod
    async def update(self, key: str, counts: str, limits: Optional[str] = None) -> None:
        """Update state based on response headers."""
        pass

class MemoryRateLimiter(AbstractRateLimiter):
    def __init__(self) -> None:
        # key -> [(completion_time, window_size)]
        self._buckets: dict[str, dict[int, list[float]]] = {}
        self._lock = asyncio.Lock()

    def _compute_wait(self, key: str, limits: List[RateLimitBucket]) -> float:
        """Compute wait time needed before a request can proceed. Must hold _lock."""
        now = time.time()
        max_wait = 0.0

        key_buckets = self._buckets.setdefault(key, {})

        for bucket in limits:
            window_requests = key_buckets.setdefault(bucket.window, [])

            # Prune old requests
            cutoff = now - bucket.window
            while window_requests and window_requests[0] <= cutoff:
                window_requests.pop(0)

            if len(window_requests) >= bucket.limit:
                oldest = window_requests[0]
                wait_time = (oldest + bucket.window) - now
                if wait_time > max_wait:
                    max_wait = wait_time

        return max_wait

    def _record_request(self, key: str, limits: List[RateLimitBucket]) -> None:
        """Record a request timestamp in all buckets. Must hold _lock."""
        now = time.time()
        for bucket in limits:
            self._buckets[key][bucket.window].append(now)

    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        while True:
            async with self._lock:
                wait = self._compute_wait(key, limits)
                if wait <= 0:
                    self._record_request(key, limits)
                    return
            # Release the lock before sleeping so other keys are not blocked
            logger.debug("Rate limit hit for %s, waiting %.2fs", key, wait)
            await asyncio.sleep(wait)

    async def update(self, key: str, counts: str, limits: Optional[str] = None) -> None:
        # MemoryRateLimiter tracks state locally; header-based updates are not needed.
        pass

class RedisRateLimiter(AbstractRateLimiter):
    def __init__(self, redis_url: str) -> None:
        if redis is None:
            raise ImportError("redis package is required for RedisRateLimiter")
        self._redis = redis.from_url(redis_url)
        
        # Lua script for atomic sliding window (Result: 0 = allowed, >0 = wait seconds)
        # ARGV[1] = current_time
        # ARGV[2] = count of buckets (N)
        # ARGV[3..3+N-1] = limits
        # ARGV[3+N..3+2N-1] = windows
        # KEYS[1..N] = keys for each bucket
        self._acquire_script = self._redis.register_script("""
            local now = tonumber(ARGV[1])
            local n_buckets = tonumber(ARGV[2])
            
            -- Check all buckets first
            for i = 1, n_buckets do
                local limit = tonumber(ARGV[2 + i])
                local window = tonumber(ARGV[2 + n_buckets + i])
                local key = KEYS[i]
                
                -- Cleanup old members
                local clear_before = now - window
                redis.call('ZREMRANGEBYSCORE', key, 0, clear_before)
                
                -- Count current
                local count = redis.call('ZCARD', key)
                
                if count >= limit then
                    -- Find oldest to determine wait
                    local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
                    local wait = 1.0 -- default fallback
                    if oldest and oldest[2] then
                        wait = (tonumber(oldest[2]) + window) - now
                    end
                    if wait < 0 then wait = 0 end
                    return tostring(wait) -- Return wait time (string for safety)
                end
            end
            
            -- Consume
            for i = 1, n_buckets do
                local key = KEYS[i]
                local window = tonumber(ARGV[2 + n_buckets + i])
                
                redis.call('ZADD', key, now, now)
                redis.call('EXPIRE', key, window + 1)
            end
            
            return "0"
        """)

    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        if not limits:
            return

        now = time.time()
        
        # Prepare keys and args
        # Use a unique key per bucket to avoid collisions when windows overlap
        # format: riot:rl:<key>:<window>
        keys = [f"riot:rl:{key}:{b.window}" for b in limits]
        limit_args = [b.limit for b in limits]
        window_args = [b.window for b in limits]
        
        args = [now, len(limits)] + limit_args + window_args
        
        # Run script
        res = await self._acquire_script(keys=keys, args=args)
        wait_time = float(res)
        
        if wait_time > 0:
            logger.debug(f"Rate limit hit for {key}, waiting {wait_time:.2f}s (Redis)")
            await asyncio.sleep(wait_time)
            # Retry
            await self.acquire(key, limits)

    async def update(self, key: str, counts: str, limits: Optional[str] = None) -> None:
        # Implementing server-side sync is complex because of "distributed" vs "local" view.
        # If we trust our Lua script, we don't strictly need to sync with headers 
        # unless we are sharing quota with apps NOT using this limiter.
        # For this "complete" wrapper, we focus on the client-side enforcement correctness.
        # Strict syncing with X-App-Rate-Limit-Count would require 'SET'ing the ZSETs 
        # which is hard because we don't know the distinct timestamps of those remote requests.
        pass
