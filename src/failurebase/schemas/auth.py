"""Authentication schemas module."""

from pydantic import BaseModel


class Token(BaseModel):
    """Schema to return data of token."""

    access_token: str
    token_type: str
    expires_minutes: int

    class Config:
        schema_extra = {
            'examples': [
                {
                    'access_token': 'eyJhbGciOiJIUsInR...sUj5Bh8Y2NjZcnZ9zM',
                    'token_type': 'bearer',
                    'expires_minutes': 15
                }
            ]
        }


class CredentialsSchema(BaseModel):
    """Schema to handle authentication data."""

    uid: str
    secret: str

    class Config:
        schema_extra = {
            'examples': [
                {
                    'uid': 'cfe0f067550e4210b5abba996d85c2bf',
                    'secret': '989b89f0628bc1afbd5923bd5d09ae4b9bca7d73b7a18d42f6b271e25b59f21b',
                }
            ]
        }
