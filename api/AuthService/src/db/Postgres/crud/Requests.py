import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.Postgres.models.UserModel import UserModel

from utils.Encryption import Encrypt



class Operations:

    @staticmethod
    async def get_item(
        session: AsyncSession, item_uuid: str | None = None, email: str | None = None
    ) -> dict:
        query = select(UserModel)
        if email:
            query = query.where(UserModel.email == email)
        elif item_uuid:
            query = query.where(UserModel.uuid == item_uuid)
        result = await session.execute(query)
        if (res:=result.scalars().first()) is not None:
            del res['password']
            return res.as_dict()

        return False
    
    @staticmethod
    async def create_item(
        session: AsyncSession, email: str, password: str, username: str
    ) -> None:
        password: str | bytes = await Encrypt.encrypt(password=password)
        new_user = UserModel(
            email=email,
            password=password,
            username=username,
            uuid=str(uuid.uuid4()),
        )
        session.add(new_user)
        await session.commit()
        return new_user.as_dict()

    