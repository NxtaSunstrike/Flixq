from typing import Annotated, Any

from faststream.redis.fastapi import RedisRouter


router = RedisRouter('redis://streamredis:5371')

def broker()->Any:
    return router.broker



