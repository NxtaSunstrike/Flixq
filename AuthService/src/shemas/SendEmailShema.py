from typing import Any
from pydantic import BaseModel, EmailStr, field_validator
from annotated_types import MinLen, MaxLen

class EmailTask(BaseModel):
    email: EmailStr
    content: str | Any