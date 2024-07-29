from typing import Any

from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.ext.asyncio import AsyncSession

from EndpActions.Register import registration
from EndpActions.Confirm import confirmation
from EndpActions.Login import login
from EndpActions.Logout import logout
from EndpActions.Refresh import Refresh


from db.Postgres.Base import get_session

from shemas.RegisterShema import UserCreate
from shemas.ConfirmShema import Confirm
from shemas.LoginShema import Login

JWTRouter = APIRouter()


@JWTRouter.post("/register")
async def RegisterUser(
    user: UserCreate, session: AsyncSession = Depends(get_session)
)->Any:
    return await registration(session=session, user=user)


@JWTRouter.post("/activate")
async def ActivateUser(
    user: Confirm, session: AsyncSession = Depends(get_session), response: Response = Response
)->Any:
    return await confirmation(session=session, user_shema=user, response=response)
    

@JWTRouter.post("/login")
async def LoginUser(
    user: Login, session: AsyncSession = Depends(get_session), response: Response = Response
)->Any:
    return await login(
        session=session, user=user, response=response
    )


@JWTRouter.delete("/logout")
async def LogoutUser(response: Response)->dict:
    return await logout(response=response)


@JWTRouter.get("/refresh")
async def RefreshToken(
    refresh: str = Cookie(default=None), session: AsyncSession = Depends(get_session)
) -> Any: 
   return await Refresh(refresh=refresh, session=session)


