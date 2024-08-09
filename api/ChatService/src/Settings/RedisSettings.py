import os
from pydantic_settings import BaseSettings
from pydantic import Field


class RedisSettings(BaseSettings):

    HOST:str = Field(os.environ.get('REDIS_HOST'))
    PORT:str = Field(os.environ.get('REDIS_PORT'))

redisSettings = RedisSettings()