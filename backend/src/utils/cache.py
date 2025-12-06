"""
Caching utilities for the Physical AI & Humanoid Robotics Textbook Platform
"""
import asyncio
import time
from typing import Any, Optional, Dict
import hashlib
import json


class CacheManager:
    """A simple in-memory cache manager with TTL support."""

    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self._cache: Dict[str, tuple] = {}  # key -> (value, timestamp)
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()

    def _is_expired(self, timestamp: float, ttl: Optional[int] = None) -> bool:
        """Check if a cached entry has expired."""
        ttl = ttl or self._default_ttl
        return (time.time() - timestamp) > ttl

    def _generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        key_data = {
            'args': args,
            'kwargs': {k: v for k, v in sorted(kwargs.items())}
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        async with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if not self._is_expired(timestamp):
                    return value
                else:
                    # Remove expired entry
                    del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache."""
        async with self._lock:
            ttl = ttl or self._default_ttl
            self._cache[key] = (value, time.time())

    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()

    async def invalidate_expired(self) -> int:
        """Remove all expired entries and return count of removed entries."""
        async with self._lock:
            expired_keys = []
            current_time = time.time()

            for key, (value, timestamp) in self._cache.items():
                if current_time - timestamp > self._default_ttl:
                    expired_keys.append(key)

            for key in expired_keys:
                del self._cache[key]

            return len(expired_keys)

    def cache(self, ttl: Optional[int] = None):
        """Decorator to cache function results."""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                cache_key = f"{func.__module__}.{func.__name__}:{self._generate_key(*args, **kwargs)}"

                # Try to get from cache
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # Execute function and cache result
                result = await func(*args, **kwargs)
                await self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator


# Global cache instance
cache_manager = CacheManager()