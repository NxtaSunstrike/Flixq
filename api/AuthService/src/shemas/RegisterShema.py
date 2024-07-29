import re
from typing import Annotated
from pydantic import BaseModel, EmailStr, field_validator
from annotated_types import MinLen, MaxLen

class UserCreate(BaseModel):
    model_config = {
        "strict": True,
        "extra": "ignore", # ignore any extra fields passed in the request body
        "json_schema_extra": {
            "examples": [
                {
                    "username": "XXXXXXX",
                    "email": "john@example.com",
                    "password": "XXXXXXXXXXX"
                }
            ]
        }
    }
    
    username: Annotated[str, MinLen(10), MaxLen(50)]
    email: EmailStr
    password: Annotated[str | bytes, MinLen(8), MaxLen(20)]

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        valid_passord = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not valid_passord.match(value):
            raise ValueError('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character')
        return value
    