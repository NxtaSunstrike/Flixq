import uuid

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.Postgres.models.UserModel import UserModel
from db.Postgres.Base import get_session

from utils.Encryption import Encrypt

from StreamPool.app import router


class Operations:

    
    @staticmethod
    async def get_item(
        item_uuid: str | None = None, email: str | None = None, DbSession: AsyncSession = Depends(get_session)
    ) -> dict | bool:
        query = select(UserModel)
        if email:
            query = query.where(UserModel.email == email)
        elif item_uuid:
            query = query.where(UserModel.uuid == item_uuid)
        result = await DbSession.execute(query)
        if (res:=result.scalars().first()) is not None:
            data = res.as_dict()
            del data['password']
            return data
        return False
    
    @staticmethod
    async def create_item(
        email: str, password: str, username: str, DbSession: AsyncSession = Depends(get_session)
    ) -> dict:
        password: str | bytes = await Encrypt.encrypt(password=password)
        new_user = UserModel(
            email=email,
            password=password,
            username=username,
            uuid=str(uuid.uuid4()),
        )
        DbSession.add(new_user)
        await DbSession.commit()
        return new_user.as_dict()

    