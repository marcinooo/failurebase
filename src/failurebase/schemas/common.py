"""Common schemas module."""

from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    """Schema to return exception to user."""

    detail: str

    class Config:
        schema_extra = {
            'examples': [
                {'detail': 'Item not found'},
            ]
        }


class PaginationSchema(BaseModel):
    """Schema to return many paginated objects."""
    items: list
    count: int
    page_number: int
    page_limit: int
    next_page: bool
    prev_page: bool

    class Config:
        schema_extra = {
            'examples': [
                {
                    'items': [{'id': 1, 'uid': 'f4a...d86'}],
                    'count': 1,
                    'page_number': 0,
                    'page_limit': 30,
                    'next_page': False,
                    'prev_page': False
                }
            ]
        }


class IdsSchema(BaseModel):
    """Schema to handle incoming objects ids to delete."""

    ids: list[int]

    class Config:
        schema_extra = {
            'examples': [
                {'ids': [4324, 8, 7623]}
            ]
        }


class StatusSchema(BaseModel):
    """Status of object processing."""

    id: int
    status: int

    class Config:
        schema_extra = {
            'examples': [
                {
                    'id': 6,
                    'status': 404
                }
            ]
        }


class StatusesSchema(BaseModel):
    """Schema to return multi status response."""

    statuses: list[StatusSchema]

    class Config:
        schema_extra = {
            'examples': [
                [{'id': 2, 'status': 200}, {'id': 5, 'status': 404}]
            ]
        }
