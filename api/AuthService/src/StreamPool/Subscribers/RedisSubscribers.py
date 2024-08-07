from fastapi import HTTPException
from faststream import Logger

from db.Redis.crud.Auth import users_cache

from StreamPool.app import router
from StreamPool.app import broker



@router.subscriber(stream = 'redisGetItem')
async def GetUser(
    key: str
)->dict | HTTPException:
    return await users_cache.get_info(key=key)

@router.subscriber(stream = 'redisAddItem')
async def AddUser(
    key: str, data: dict
)->dict | HTTPException:
    return await users_cache.set_info(key=key, data=data)
