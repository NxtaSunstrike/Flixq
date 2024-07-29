from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings.AppSettings import FastAPI_Settings

print(FastAPI_Settings.model_dump())

engine = create_async_engine(
    url= f"postgresql+asyncpg://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}",
    echo=True,
)


class Base(DeclarativeBase):
    pass

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session