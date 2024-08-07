import os
from pydantic_settings import BaseSettings
from pydantic import Field


class RedisSettings(BaseSettings):

    HOST:str = Field('localhost')
    PORT:str = Field('5397')

redisSettings = RedisSettings()