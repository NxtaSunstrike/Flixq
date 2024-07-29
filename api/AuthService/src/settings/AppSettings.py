from pydantic import (
    Field
)

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    

    #Postgres
    POSTGRES: str = Field(
        f"postgresql+asyncpg://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
    )

    CELERY_RESULT_BACKEND: str =Field(os.environ.get('CELERY_RESULT_BACKEND'))
    CELERY_BROKER_URL: str = Field(os.environ.get('CELRY_BROKER_URL'))

    #REDIS
    REDIS: str = Field(f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}")
    REDIS_CHATS: str = (f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/3")
    REDIS_USERS: str = Field(f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/4")


    #salts
    SALT: str = Field(os.environ.get('salt'))

FastAPI_Settings = AppSettings()