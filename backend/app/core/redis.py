import json
import logging
from typing import Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# Lazy redis connection
_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        try:
            import redis
            _redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test ping
            _redis_client.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.warning(f"Redis not available ({e}). Cache will be bypassed.")
            _redis_client = False
    return _redis_client if _redis_client is not False else None

def get_cache(key: str) -> Optional[Any]:
    """Fetch and decode cached JSON by key."""
    client = get_redis_client()
    if not client:
        return None
    try:
        data = client.get(key)
        return json.loads(data) if data else None
    except Exception as e:
        logger.warning(f"Redis get_cache error: {e}")
        return None

def set_cache(key: str, value: Any, expire_seconds: int = 300) -> bool:
    """Store data as JSON in Redis with expiration in seconds (default 5 mins)."""
    client = get_redis_client()
    if not client:
        return False
    try:
        client.setex(key, expire_seconds, json.dumps(value, default=str))
        return True
    except Exception as e:
        logger.warning(f"Redis set_cache error: {e}")
        return False

def delete_cache(key: str) -> bool:
    """Delete a specific cache key."""
    client = get_redis_client()
    if not client:
        return False
    try:
        client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Redis delete_cache error: {e}")
        return False

def delete_cache_pattern(pattern: str) -> bool:
    """Delete all keys matching a wildcard pattern (e.g., 'categories:*')."""
    client = get_redis_client()
    if not client:
        return False
    try:
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
        return True
    except Exception as e:
        logger.warning(f"Redis delete_cache_pattern error: {e}")
        return False
