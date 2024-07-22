from pydantic import (
    Field
)

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env-non-dev",
    )

    #Postgres
    POSTGRES: str = Field(
        f'postgresql+asyncpg://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}'
    )

    #REDIS
    REDIS: str = Field(f'redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}')
    REDIS_CHATS: str = (f'redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/3')
    REDIS_USERS: str = Field(f'redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/4')

    RABBIT: str = Field(f'amqp://{os.environ.get('RABBIT_USER')}:{os.environ.get('RABBIT_PASSWORD')}@{os.environ.get('RABBIT_HOST')}:{os.environ.get('RABBIT_PORT')}')

    NATS: str = Field(f'nats://{os.environ.get('NATS_HOST')}:{os.environ.get('NATS_PORT')}')

    #salts
    SALT: str = Field(os.environ.get('salt'))

FastAPI_Settings = AppSettings()