from pydantic import BaseModel, EmailStr, field_validator

class Confirm(BaseModel):
    model_config = {
        "strict": True,
        "extra": "ignore", # ignore any extra fields passed in the request body
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john@example.com",
                    "code": 123456
                }
            ]
        }
    }
    code: int
    email: EmailStr

    @field_validator('code')
    @classmethod
    def validate_code(cls, value):
        if len(str(value)) != 6:
            raise ValueError('Code must be 6 digits long')
        return value