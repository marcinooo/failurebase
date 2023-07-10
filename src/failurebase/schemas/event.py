"""Event schemas module."""

from datetime import datetime
from pydantic import BaseModel, validator

from .test import CreateTestSchema, GetTestSchema


create_event_schema_example = {
    'test': {
        'uid': 'Test.Test Demo',
        'marks': ['CRT'],
        'file': '/home/anakin/skywalker/test.robot'
    },
    'message': "Resolving variable '${1 / 0}' failed: ZeroDivisionError: division by zero",
    'traceback': "Resolving variable '${1 / 0}' failed: ZeroDivisionError: division by zero",
    'client_timestamp': '2023-06-14T12:43:51.750000',
    'server_timestamp': '2023-06-14T12:43:52.520534'
}


class CreateEventSchema(BaseModel):
    """Schema to handle incoming data of event."""

    test: CreateTestSchema
    message: str
    traceback: str
    timestamp: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': create_event_schema_example
        }

    @validator('timestamp')
    def timestamp_should_be_string_or_datetime(cls, v):
        """Validates timestamp string format."""

        datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
        return v

    @property
    def deserialized_timestamp(self):
        """Dumps timestamp string to datetime object."""

        return datetime.strptime(self.timestamp, '%Y-%m-%dT%H:%M:%S.%f')


class GetEventSchema(BaseModel):
    """Schema to return data of event to client."""

    id: int
    test: GetTestSchema
    message: str
    traceback: str
    client_timestamp: datetime
    server_timestamp: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f')
        }


class GetEventsSchema(BaseModel):
    """Schema to return list of events to client."""

    events: list[GetEventSchema]
    page_number: int
    page_limit: int
