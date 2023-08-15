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
        schema_extra = {
            'examples': [
                {
                    'uid': 'Test.Test Example',
                    'marks': ['CIT'],
                    'file': '/home/obi/wan/kenobi/test.robot'
                }
            ]
        }

    @property
    def serialized_marks(self):
        """Dumps list of marks to json string."""

        return json.dumps(self.marks)


class GetTestSchema(BaseModel):
    """Schema to return data of test to user."""

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
        schema_extra = {
            'examples': [
                {
                    'id': 1,
                    'uid': 'Test.Test Example',
                    'marks': '["CIT"]',
                    'file': '/home/obi/wan/kenobi/test.robot',
                    'total_events_count': 12
                }
            ]
        }
