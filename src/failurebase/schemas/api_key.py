"""ApiKey schemas module."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class GetApiKeySchema(BaseModel):
    """Schema to return data of api key."""

    encrypted_value: str
    created: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            'examples': [
                {
                    'encrypted_value': 'eyJhbGciOiJIUsInR...sUj5Bh8Y2NjZcnZ9zM',
                    'created': '2023-07-11T11:12:13.340000'
                }
            ]
        }


class CreateApiKeySchema(BaseModel):
    """Schema to handle data of api key."""

    value: str
    created: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True
        schema_extra = {
            'examples': [
                {
                    'value': 'Sec91.val?O0'
                },
                {
                    'value': '!tSh0uldBeStr0ng',
                    'created': '2023-07-11T11:12:13.340000'
                }
            ]
        }
