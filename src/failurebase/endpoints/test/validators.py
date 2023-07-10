from enum import Enum


class TestsOrder(Enum):
    """Possible values of ordering query parameter."""

    ASC_UID: str = 'uid'
    DESC_UID: str = '-uid'

    ASC_FILE: str = 'file'
    DESC_FILE: str = '-file'

    ASC_TOTAL_EVENTS_COUNT: str = 'total_events_count'
    DESC_TOTAL_EVENTS_COUNT: str = '-total_events_count'
