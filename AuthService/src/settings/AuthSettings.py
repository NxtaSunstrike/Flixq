from pydantic import (
    Field
)

from pathlib import Path

from pydantic_settings import BaseSettings

KEYS_DIR = Path(__file__).parent.parent.parent

print(KEYS_DIR)

class JWTSettings(BaseSettings):
    secret: Path = KEYS_DIR / 'jwt-private.pem'
    public: Path = KEYS_DIR / 'jwt-public.pem'
    algorithm: str = Field('RS256')
    expire_minutes: int = Field(15)
    expire_days: int = Field(30)


JWTSet = JWTSettings()