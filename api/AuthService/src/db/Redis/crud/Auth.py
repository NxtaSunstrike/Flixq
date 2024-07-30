import json 
from fastapi import HTTPException
from redis.asyncio import Redis
from settings.AppSettings import FastAPI_Settings


class SessionAuth:


    def __init__(self, redis_url: str) -> None:
        self.client: Redis = Redis.from_url(redis_url)

    async def set_info(
        self, key: str, data: dict
    )->dict | HTTPException:
        try:
            await self.client.set(key, json.dumps(data))
            return {"message": 'ok'}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    async def get_info(
        self, key: str
    )->dict | HTTPException:
        try: 
            res = await self.client.get(key)
            if res:
                data = json.loads(res)
                return data
            return {}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

    async def del_info(
        self, key: str
    )->dict | HTTPException:
        try:
            await self.client.delete(key)
            return {"message": 'ok'}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


users_cache = SessionAuth(redis_url=FastAPI_Settings.REDIS_USERS)
auth_cache = SessionAuth(redis_url=FastAPI_Settings.REDIS)