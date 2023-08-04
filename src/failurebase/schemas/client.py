from datetime import datetime
from pydantic import BaseModel, SecretStr, Field


class GetClientSchema(BaseModel):
    """Schema to return data of client with mocked secret."""

    id: int
    uid: str
    secret: SecretStr
    created: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f')
        }


class CreateClientSchema(BaseModel):
    """Schema to handle data of client."""

    uid: str
    secret: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': '..'
        }
