"""Common schemas module."""

from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    """Schema to return exception to user."""

    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'Item not found'},
        }


class PaginationSchema(BaseModel):
    """Schema to return many paginated objects."""
    items: list
    count: int
    page_number: int
    page_limit: int
    next_page: bool
    prev_page: bool


class StatusSchema(BaseModel):
    """Status of object processing."""

    id: int
    status: int


class IdsSchema(BaseModel):
    """Schema to handle incoming objects ids to delete."""

    ids: list[int]


class StatusesSchema(BaseModel):
    """Schema to return multi status response."""

    statuses: list[StatusSchema]
