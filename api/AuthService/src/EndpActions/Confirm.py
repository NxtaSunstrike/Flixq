from typing import Any

from fastapi import HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shemas.ConfirmShema import Confirm

from utils.JWT import TokenActions

from db.Postgres.Base import get_session
from db.Postgres.crud.Requests import Operations
from db.Redis.crud.Auth import users_cache, auth_cache


async def confirmation(
    user_shema: Confirm, response: Response, DbSession: AsyncSession = Depends(get_session)
)->dict[str | Any] | HTTPException:
    data = await auth_cache.get_info(key=user_shema.email)
    try:
        user = data['user']
        if data['code'] == user_shema.code:
            user: dict = await Operations.create_item(
                DbSession=DbSession, email=user['email'], password=user['password'], username=user['name']
            )
            await auth_cache.del_info(key=user_shema.email)
            await users_cache.set_info(key=user['email'], data=user)
            response.set_cookie(
                key = "refresh",
                value = await TokenActions.generate_jwt(
                        payload={
                            'sub': user['uuid'],
                            'name': user['username']
                        },
                        token_type='refresh'
                    ),
                httponly=True
            )
            del user['password']
            payload = user.copy()
            user.update({
                'sub': user['uuid']
            })            
            return {
                'user': user, 
                'access' : await TokenActions.generate_jwt(payload=payload, token_type='access')
            }
    except KeyError:
        raise HTTPException(status_code=400, detail="user not found")
    raise HTTPException(status_code=400, detail="Invalid code")