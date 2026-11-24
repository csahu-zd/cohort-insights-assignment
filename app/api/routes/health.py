import logging

from fastapi import APIRouter, Response, status
from pymongo.errors import PyMongoError
from redis.exceptions import RedisError

from app.db.mongodb import database
from app.db.redis import redis

router = APIRouter(tags=["health"])
logger = logging.getLogger("cohort.api")


@router.get("/health")
async def health(response: Response):
    checks = {}
    try:
        await database.command("ping")
        checks["mongodb"] = "ok"
    except PyMongoError:
        logger.exception("Health check: MongoDB down")
        checks["mongodb"] = "down"
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except RedisError:
        logger.exception("Health check: Redis down")
        checks["redis"] = "down"
    if "down" in checks.values():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return checks
