"""Event validators module."""

from typing import Annotated
from datetime import datetime
from enum import Enum
from fastapi import Query

from ..validators import RequestValidationError


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


def validate_start_server_timestamp(
    start_server_timestamp: Annotated[
        str | None, Query(title='Start Server Timestamp', description='Indicates the date from which to start '
                                                                      'filtering.')
    ] = None
) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    return validate_timestamp('start_server_timestamp', start_server_timestamp)


def validate_end_server_timestamp(
    end_server_timestamp: Annotated[
        str | None, Query(title='End Server Timestamp', description='Indicates the date on which to stop filtering.')
    ] = None
) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    return validate_timestamp('end_server_timestamp', end_server_timestamp)


def validate_start_client_timestamp(
    start_client_timestamp: Annotated[
        str | None, Query(title='Start Client Timestamp', description='Indicates the date from which to start '
                                                                      'filtering.')
    ] = None
) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    return validate_timestamp('start_client_timestamp', start_client_timestamp)


def validate_end_client_timestamp(
    end_client_timestamp: Annotated[
        str | None, Query(title='End Client Timestamp', description='Indicates the date on which to stop filtering.')
    ] = None
) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    return validate_timestamp('end_client_timestamp', end_client_timestamp)


class EventsOrder(Enum):
    """Possible values of ordering query parameter."""

    ASC_MESSAGE: str = 'message'
    DESC_MESSAGE: str = '-message'

    ASC_SERVER_TIMESTAMP: str = 'server_timestamp'
    DESC_SERVER_TIMESTAMP: str = '-server_timestamp'

    ASC_CLIENT_TIMESTAMP: str = 'client_timestamp'
    DESC_CLIENT_TIMESTAMP: str = '-client_timestamp'

    ASC_TEST_UID: str = 'test_uid'
    DESC_TEST_UID: str = '-test_uid'
