from fastapi import HTTPException, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils.JWT import TokenActions
from db.Postgres.Base import get_session


async def Refresh(
    refresh: str  = Cookie(default=None), session: AsyncSession = Depends(get_session)
) -> dict[str, str] | HTTPException:
    if not refresh:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await TokenActions.Refresh(token=refresh, type='refresh', session=session)