"""Client schemas module."""

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
        schema_extra = {
            'examples': [
                {
                    'id': 1,
                    'uid': 'a5322e89a7cb49a58d814029b9997a29',
                    'secret': '**********',
                    'created': '2023-07-12T12:13:14.450000'
                },
                {
                    'id': 1,
                    'uid': 'cfe0f067550e4210b5abba996d85c2bf',
                    'secret': '989b89f0628bc1afbd5923bd5d09ae4b9bca7d73b7a18d42f6b271e25b59f21b',
                    'created': '2023-07-13T14:15:16.560000'
                }
            ]
        }


class CreateClientSchema(BaseModel):
    """Schema to handle data of client."""

    uid: str
    secret: str

    class Config:
        orm_mode = True
        schema_extra = {
            'examples': [
                {
                    'uid': 'cfe0f067550e4210b5abba996d85c2bf',
                    'secret': '989b89f0628bc1afbd5923bd5d09ae4b9bca7d73b7a18d42f6b271e25b59f21b'
                }
            ]
        }
