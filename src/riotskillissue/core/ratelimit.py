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

    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        async with self._lock:
            now = time.time()
            max_wait = 0.0
            
            # Check all buckets for this key
            key_buckets = self._buckets.setdefault(key, {})
            
            for bucket in limits:
                window_requests = key_buckets.setdefault(bucket.window, [])
                
                # Prune old requests
                cutoff = now - bucket.window
                while window_requests and window_requests[0] <= cutoff:
                    window_requests.pop(0)
                
                # Update list after prune
                key_buckets[bucket.window] = window_requests
                
                if len(window_requests) >= bucket.limit:
                    # Determine wait time: time until the oldest request expires
                    oldest = window_requests[0]
                    # We need to wait until (oldest + window) - now
                    wait_time = (oldest + bucket.window) - now
                    if wait_time > max_wait:
                        max_wait = wait_time

            if max_wait > 0:
                logger.debug(f"Rate limit hit for {key}, waiting {max_wait:.2f}s")
                await asyncio.sleep(max_wait)
                # Recursive retry to ensure clean state after sleep (could be racing)
                # But for simple memory impl, we assume we just consumed the slot.
                # Actually proper impl requires re-check or reservation.
                # For simplicity here, we assume reservation logic:
            
            # Reserve spot
            now = time.time() # Update time after sleep
            for bucket in limits:
                self._buckets[key][bucket.window].append(now)

    async def update(self, key: str, counts: str, limits: Optional[str] = None) -> None:
        # Memory limiter is self-contained, but we could sync with headers if we drifted.
        # For this implementation, we trust our local count more due to race conditions with distributed headers,
        # UNLESS we are strictly respecting headers which might be "future" from other nodes.
        # But simple MemoryLimiter is usually single-process.
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
        # We use a unique key for each bucket definition to avoid collision if windows overlap weirdly
        # format: riot:ratelimit:<key>:<window>
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
