"""Event handlers module."""

from logging import getLogger
from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from failurebase.endpoints.event.validators import (validate_start_server_timestamp, validate_end_server_timestamp,
                                                    validate_start_client_timestamp, validate_end_client_timestamp,
                                                    EventsOrder)
from failurebase.services.event.service import EventService
from failurebase.containers import Application
from failurebase.schemas.event import CreateEventSchema, GetEventSchema
from failurebase.schemas.client import GetClientSchema
from failurebase.schemas.common import HTTPExceptionSchema, IdsSchema, StatusesSchema, PaginationSchema
from failurebase.adapters.exceptions import NotFoundError
from failurebase.endpoints.auth.utils import get_current_client, get_api_key


logger = getLogger(__name__)

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

    test_mark: Annotated[
        list[str] | None, Query(title='Test mark', description='Mark of test.', max_length=2000)
    ] = None,

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

    paginated_events = event_service.get_many(
        page, page_limit, start_server_timestamp=start_server_timestamp, end_server_timestamp=end_server_timestamp,
        start_client_timestamp=start_client_timestamp, end_client_timestamp=end_client_timestamp, message=message,
        traceback=traceback, test_uid=test_uid, test_marks=test_mark, test_file=test_file, ordering=ordering
    )

    json_compatible_content = jsonable_encoder(paginated_events)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.post(
    '/events',
    responses={
        201: {'model': GetEventSchema, 'description': 'Created item'},
    }
)
@inject
def create_event(

    event_schema: CreateEventSchema,

    event_service: EventService = Depends(Provide[Application.services.event_service]),

    client: GetClientSchema = Depends(get_current_client),

) -> Response:
    """Creates new event and test (if it is required)."""

    event = event_service.create(event_schema, client)

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
    """Returns event with passed ID."""

    try:
        event = event_service.get_one_by_id(event_id)
    except NotFoundError:
        logger.error('Event with id %s was not found', event_id)
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

    api_key: str = Depends(get_api_key)

) -> Response:
    """Delete events with passed IDs."""

    results = event_service.delete(ids_schema)

    json_compatible_content = jsonable_encoder(results)
    return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=json_compatible_content)
