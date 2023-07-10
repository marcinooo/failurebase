"""Test schemas module."""

import json
from pydantic import BaseModel, Json


class CreateTestSchema(BaseModel):
    """Schema to handle incoming data of test in event."""

    uid: str
    marks: list[str]
    file: str

    class Config:
        orm_mode = True

    @property
    def serialized_marks(self):
        """Dumps list of marks to json string."""

        return json.dumps(self.marks)


class GetTestSchema(BaseModel):
    """Schema to return data of test to client."""

    id: int
    uid: str
    marks: Json
    file: str
    total_events_count: int

    class Config:
        orm_mode = True
        json_encoders = {
            Json: lambda v: json.loads(v.marks)
        }


class GetTestsSchema(BaseModel):
    """Schema to return list of tests to client."""

    tests: list[GetTestSchema]
    page_number: int
    page_limit: int
