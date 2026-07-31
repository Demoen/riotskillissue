from __future__ import annotations

import asyncio
import logging
import math
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

try:
    import redis.asyncio as redis
except ImportError:
    redis = None  # type: ignore

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RateLimitBucket:
    limit: int
    window: int

    def __post_init__(self) -> None:
        if self.limit <= 0 or self.window <= 0:
            raise ValueError("rate-limit values must be positive")

    def __repr__(self) -> str:
        return f"{self.limit}:{self.window}"


def _parse_pairs(header_value: str, *, allow_zero: bool) -> List[Tuple[int, int]]:
    pairs: List[Tuple[int, int]] = []
    for part in header_value.split(","):
        fields = part.strip().split(":")
        if len(fields) != 2:
            continue
        try:
            first, window = (int(field.strip()) for field in fields)
        except ValueError:
            continue
        if window <= 0 or first < 0 or (first == 0 and not allow_zero):
            continue
        pairs.append((first, window))
    return pairs


def parse_rate_limits(header_value: str) -> List[RateLimitBucket]:
    if not header_value:
        return []
    return [
        RateLimitBucket(limit, window)
        for limit, window in _parse_pairs(header_value, allow_zero=False)
    ]


def parse_rate_limit_counts(header_value: str) -> List[Tuple[int, int]]:
    if not header_value:
        return []
    return _parse_pairs(header_value, allow_zero=True)


class AbstractRateLimiter(ABC):
    @abstractmethod
    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, key: str, counts: str, limits: Optional[str] = None
    ) -> None:
        raise NotImplementedError


class MemoryRateLimiter(AbstractRateLimiter):
    def __init__(self) -> None:
        self._buckets: dict[str, dict[int, list[float]]] = {}
        self._lock = asyncio.Lock()

    def _compute_wait(
        self, key: str, limits: List[RateLimitBucket], now: float
    ) -> float:
        max_wait = 0.0
        key_buckets = self._buckets.setdefault(key, {})

        for bucket in limits:
            requests = key_buckets.setdefault(bucket.window, [])
            cutoff = now - bucket.window
            while requests and requests[0] <= cutoff:
                requests.pop(0)
            if len(requests) >= bucket.limit:
                max_wait = max(max_wait, requests[0] + bucket.window - now)

        return max_wait

    def _record_request(
        self, key: str, limits: List[RateLimitBucket], now: float
    ) -> None:
        key_buckets = self._buckets.setdefault(key, {})
        for bucket in limits:
            key_buckets.setdefault(bucket.window, []).append(now)

    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        if not limits:
            return
        while True:
            async with self._lock:
                now = time.monotonic()
                wait = self._compute_wait(key, limits, now)
                if wait <= 0:
                    self._record_request(key, limits, now)
                    return
            logger.debug("Rate limit reached for %s; waiting %.2fs", key, wait)
            await asyncio.sleep(wait)

    async def update(
        self, key: str, counts: str, limits: Optional[str] = None
    ) -> None:
        parsed_counts = parse_rate_limit_counts(counts)
        if not parsed_counts:
            return
        allowed_windows = (
            {bucket.window for bucket in parse_rate_limits(limits)}
            if limits
            else None
        )
        async with self._lock:
            now = time.monotonic()
            key_buckets = self._buckets.setdefault(key, {})
            for count, window in parsed_counts:
                if allowed_windows is not None and window not in allowed_windows:
                    continue
                requests = key_buckets.setdefault(window, [])
                cutoff = now - window
                while requests and requests[0] <= cutoff:
                    requests.pop(0)
                if count > len(requests):
                    requests.extend([now] * (count - len(requests)))


class RedisRateLimiter(AbstractRateLimiter):
    def __init__(self, redis_url: str) -> None:
        if redis is None:
            raise ImportError("redis package is required for RedisRateLimiter")
        self._redis = redis.from_url(redis_url)
        self._acquire_script = self._redis.register_script(
            """
            local now = tonumber(ARGV[1])
            local n_buckets = tonumber(ARGV[2])
            local member = ARGV[3]

            for i = 1, n_buckets do
                local limit = tonumber(ARGV[3 + i])
                local window = tonumber(ARGV[3 + n_buckets + i])
                local key = KEYS[i]
                redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
                local count = redis.call('ZCARD', key)
                if count >= limit then
                    local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
                    local wait = 1.0
                    if oldest and oldest[2] then
                        wait = (tonumber(oldest[2]) + window) - now
                    end
                    if wait < 0 then wait = 0 end
                    return tostring(wait)
                end
            end

            for i = 1, n_buckets do
                local key = KEYS[i]
                local window = tonumber(ARGV[3 + n_buckets + i])
                redis.call('ZADD', key, now, member .. ':' .. tostring(i))
                redis.call('EXPIRE', key, math.ceil(window) + 1)
            end

            return "0"
            """
        )

    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        if not limits:
            return
        keys = [f"riot:rl:{key}:{bucket.window}" for bucket in limits]
        limit_args = [bucket.limit for bucket in limits]
        window_args = [bucket.window for bucket in limits]

        while True:
            now = time.time()
            member = uuid.uuid4().hex
            args: List[Union[str, int, float]] = [
                now,
                len(limits),
                member,
                *limit_args,
                *window_args,
            ]
            result = await self._acquire_script(keys=keys, args=args)
            try:
                wait = float(result)
            except (TypeError, ValueError):
                wait = 0.0
            if not math.isfinite(wait) or wait <= 0:
                return
            logger.debug("Rate limit reached for %s; waiting %.2fs", key, wait)
            await asyncio.sleep(wait)

    async def update(
        self, key: str, counts: str, limits: Optional[str] = None
    ) -> None:
        return None
