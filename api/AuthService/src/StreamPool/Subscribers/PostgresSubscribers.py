from StreamPool.app import router

from db.Postgres.Base import get_session
from db.Postgres.crud.Requests import Operations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


    
@router.subscriber(stream='PostgresGetUser')
async def getItem(
    itemUUID: str | None = None, email: str | None = None, DbSession:AsyncSession = Depends(get_session)
)->dict | bool:
    if itemUUID:
        return await Operations.get_item(item_uuid=itemUUID, DbSession=DbSession)
    elif email:
        return await Operations.get_item(email=email, DbSession=DbSession)