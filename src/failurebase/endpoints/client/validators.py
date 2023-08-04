"""Event validators module."""

from typing import Annotated
from datetime import datetime
from enum import Enum
from fastapi import Query

from ..validators import validate_timestamp


def validate_start_created(
    start_created: Annotated[
        str | None, Query(title='Created Client Timestamp',
                          description='Indicates the date on which to start filtering.')
    ] = None
) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    return validate_timestamp('start_created', start_created)


def validate_end_created(
    end_created: Annotated[
        str | None, Query(title='Created Client Timestamp',
                          description='Indicates the date on which to end filtering.')
    ] = None
) -> datetime | None:
    """Validates if received query parameter has expected datetime format."""

    return validate_timestamp('end_created', end_created)


class ClientsOrder(Enum):
    """Possible values of ordering query parameter."""

    ASC_UID: str = 'uid'
    DESC_UID: str = '-uid'

    ASC_CREATED: str = 'created'
    DESC_CREATED: str = '-created'
