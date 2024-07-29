from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    model_config = {
        "strict": True,
        "extra": "ignore", # ignore any extra fields passed in the request body
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john@example.com",
                    "password": "XXXXXXXXXXX"
                }
            ]
        }
    }
    email: EmailStr
    password: str