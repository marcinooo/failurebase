"""Common validators module."""

from datetime import datetime
from fastapi import HTTPException


class RequestValidationError(HTTPException):
    """Validation error of query params."""

    def __init__(self, loc, msg, typ):
        super().__init__(422, [{'loc': loc, 'msg': msg, 'type': typ}])


def validate_timestamp(parameter_name: str, timestamp: str | None = None) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    if timestamp is not None:
        try:
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            raise RequestValidationError(
                ('path', parameter_name),
                'string does not match format: %Y-%m-%dT%H:%M:%S.%f',
                'value_error.timestamp.format'
            ) from None
