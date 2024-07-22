from typing import Any
from random import sample

from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from shemas.RegisterShema import UserCreate

from tasks.tasks import router

from faststream.rabbit import RabbitBroker

from db.Postgres.Base import get_session
from db.Redis.crud.Auth import users_cache, auth_cache
from db.Postgres.crud.Requests import Operations


async def registration(
        user: UserCreate, session: AsyncSession = Depends(get_session)
) -> dict[str | Any] | HTTPException:
    if not len(await users_cache.get_info(key=user.email)):
        if not await Operations.get_item(session=session, email=user.email):
            user_data = {
                'code': int(''.join(sample('123456789', 6))),
                'user':  {
                        "name": user.username,
                        "email": user.email,
                        "password": user.password
                    }
                }
            await auth_cache.set_info(key=user.email, data=user_data)
            task = await router.broker.publish(
                message={'email': user.email, 'content': user_data['code']},
                channel='tasks'
            )
            return JSONResponse(
                    {'message': 'Confirmation code has been sent to your email'},
                    background=task
                )
        raise HTTPException(status_code=400, detail="User already exists")
    raise HTTPException(status_code=400, detail="User already exists")
    

