from pydantic import (
    Field
)

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class TasksSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env-non-dev",
    )

    # RABBIT: str = Field(f'amqp://{os.environ.get('RABBIT_USER')}:{os.environ.get('RABBIT_PASSWORD')}@{os.environ.get('RABBIT_HOST')}:{os.environ.get('RABBIT_PORT')}')

    EMAIL_HOST: str = Field('smtp.gmail.com')
    EMAIL_PORT: int = Field(os.environ.get('EMAIL_PORT'))
    EMAIL_USER: str = Field(os.environ.get('EMAIL_USER'))
    EMAIL_PASSWORD: str = Field(os.environ.get('EMAIL_PASSWORD'))
    
tasksSettings = TasksSettings()