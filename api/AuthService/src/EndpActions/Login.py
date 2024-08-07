from fastapi import HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shemas.LoginShema import Login

from utils.Encryption import Encrypt
from utils.JWT import TokenActions
from utils.Login import LoginActions

from db.Postgres.Base import get_session
from db.Postgres.crud.Requests import Operations
from db.Redis.crud.Auth import users_cache


async def login(
    user: Login, response: Response, DbSession: AsyncSession = Depends(get_session)
) -> None:
    if len(user_info:=await users_cache.get_info(key=user.email)):
        if await Encrypt.encrypt(user.password) == user_info['password']:
            return await LoginActions(
                response=response, user_info=user_info
            )
        raise HTTPException(status_code=401, detail="Invalid password")

    elif (user_info:=await Operations.get_item(DbSession=DbSession, email=user.email)):
        if await Encrypt.encrypt(user.password) == user_info['password']:
            return await LoginActions(
                response=response, user_info=user_info
            )
        raise HTTPException(status_code=401, detail="Invalid password")
    raise HTTPException(status_code=400, detail="User not found")