from typing import Any
from random import sample

from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from shemas.RegisterShema import UserCreate

from tasks.tasks import send_email


from db.Postgres.Base import get_session
from db.Redis.crud.Auth import users_cache, auth_cache
from db.Postgres.crud.Requests import Operations


async def registration(
        user: UserCreate, DbSession: AsyncSession = Depends(get_session)
) -> dict[str | Any] | HTTPException:
    if not len(await users_cache.get_info(key=user.email)):
        if not await Operations.get_item(DbSession=DbSession, email=user.email):
            user_data = {
                'code': int(''.join(sample('123456789', 6))),
                'user':  {
                        "name": user.username,
                        "email": user.email,
                        "password": user.password
                    }
                }
            await auth_cache.set_info(key=user.email, data=user_data)
            send_email.delay(email = user.email, content = str(user_data['code']))
            return {'message': 'Confirmation code has been sent to your email'}
                
        raise HTTPException(status_code=400, detail="User already exists")
    raise HTTPException(status_code=400, detail="User already exists")
    

