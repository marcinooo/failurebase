"""Event handlers module."""

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from .validators import (validate_start_server_timestamp, validate_end_server_timestamp,
                         validate_start_client_timestamp, validate_end_client_timestamp, EventsOrder)
from ..validators import validate_test_marks
from ...services.event import EventService
from ...containers import Application
from ...schemas.event import CreateEventSchema, GetEventSchema
from ...schemas.common import HTTPExceptionSchema, IdsSchema, StatusesSchema, PaginationSchema
from ...adapters.exceptions import NotFoundError


router = APIRouter()


@router.get(
    '/events',
    responses={
        200: {'model': PaginationSchema, 'description': 'Requested items'}
    }
)
@inject
def get_events(

    page: Annotated[
        int, Query(title='Page number', description='The list of returned objects is broken down into smaller '
                                                    'chunks that can be retrieved via the page index.')
    ] = 0,

    start_server_timestamp: datetime | None = Depends(validate_start_server_timestamp),

    end_server_timestamp: datetime | None = Depends(validate_end_server_timestamp),

    start_client_timestamp: datetime | None = Depends(validate_start_client_timestamp),

    end_client_timestamp: datetime | None = Depends(validate_end_client_timestamp),

    message: Annotated[
        str | None, Query(title='Failure Message', description='Error message as a cause of failure.', max_length=2000)
    ] = None,

    traceback: Annotated[
        str | None, Query(title='Traceback Of Error', description='Additional information of failure.', max_length=3000)
    ] = None,

    test_uid: Annotated[
        str | None, Query(title='Test UID', description='Unique identifier of test.', max_length=2000)
    ] = None,

    test_marks: list[str] | None = Depends(validate_test_marks),

    test_file: Annotated[
        str | None, Query(title='Test File Path', description='File path of test.', max_length=1000)
    ] = None,

    ordering: Annotated[
        str | None, Query(title='Order By Given Column',
                          description='Events will be sorted by given event or test property.',
                          regex=f'^({"|".join(o.value for o in EventsOrder)})$')
    ] = None,

    event_service: EventService = Depends(Provide[Application.services.event_service]),

    page_limit: int = Depends(Provide[Application.config.EVENTS_PER_PAGE])

) -> Response:
    """Returns events per given page."""

    paginated_events = event_service.get_many(page, page_limit, start_server_timestamp, end_server_timestamp,
                                              start_client_timestamp, end_client_timestamp, message, traceback,
                                              test_uid, test_marks, test_file, ordering)

    json_compatible_content = jsonable_encoder(paginated_events)
    import time
    time.sleep(1)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.post(
    '/events',
    responses={
        200: {'model': GetEventSchema, 'description': 'Created item'},
    }
)
@inject
def create_event(

    event_schema: CreateEventSchema,

    event_service: EventService = Depends(Provide[Application.services.event_service]),

) -> Response:
    """Creates new event and test (if it is required)."""

    event = event_service.create(event_schema)
    json_compatible_content = jsonable_encoder(event)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_compatible_content)


@router.get(
    '/events/{event_id}',
    responses={
        200: {'model': GetEventSchema, 'description': 'Item requested by ID'},
        404: {'model': HTTPExceptionSchema, 'description': 'Item was not found'},
    }
)
@inject
def get_event(

    event_id: int,

    event_service: EventService = Depends(Provide[Application.services.event_service]),

) -> Response:
    """Item returned by requested ID."""

    try:
        event = event_service.get_one(event_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event with ID "{event_id}" was not found')
    else:
        json_compatible_content = jsonable_encoder(event)
        return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.post(  # DELETE can be blocked by proxy server
    '/events/delete',
    responses={
        207: {'model': StatusesSchema, 'description': 'List of deletion statuses for each processed object.'},
    }
)
@inject
def delete(

    ids_schema: IdsSchema,

    event_service: EventService = Depends(Provide[Application.services.event_service]),

) -> Response:
    """Items deleted by passed IDs."""

    results = event_service.delete(ids_schema)

    json_compatible_content = jsonable_encoder(results)
    return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=json_compatible_content)
