from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class GetApiKeySchema(BaseModel):
    encrypted_value: str
    created: datetime

    class Config:
        orm_mode = True


class CreateApiKeySchema(BaseModel):
    value: str
    created: Optional[datetime] = datetime.now()
