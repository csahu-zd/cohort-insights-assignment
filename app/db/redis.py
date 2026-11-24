from redis.asyncio import Redis

from app.core.config import REDIS_URL

redis = Redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=1, socket_connect_timeout=1)
