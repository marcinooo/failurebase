"""Client handlers module."""

import uuid
import secrets
from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from failurebase.endpoints.client.validators import validate_start_created, validate_end_created, ClientsOrder
from failurebase.services.client.service import ClientService
from failurebase.managers.secret import SecretManager
from failurebase.containers import Application
from failurebase.schemas.client import GetClientSchema, CreateClientSchema
from failurebase.schemas.common import HTTPExceptionSchema, IdsSchema, StatusesSchema, PaginationSchema
from failurebase.adapters.exceptions import NotFoundError
from failurebase.endpoints.auth.utils import get_api_key


router = APIRouter()


@router.get(
    '/clients',
    responses={
        200: {'model': PaginationSchema, 'description': 'Requested items'}
    }
)
@inject
def get_clients(

    page: Annotated[
        int, Query(title='Page number', description='The list of returned objects is broken down into smaller '
                                                    'chunks that can be retrieved via the page index.')
    ] = 0,

    start_created: datetime | None = Depends(validate_start_created),

    end_created: datetime | None = Depends(validate_end_created),

    uid: Annotated[
        str | None, Query(title='Test UID', description='Unique identifier of client.', max_length=32)
    ] = None,

    ordering: Annotated[
        str | None, Query(title='Order By Given Column',
                          description='Events will be sorted by given event or test property.',
                          regex=f'^({"|".join(o.value for o in ClientsOrder)})$')
    ] = None,

    client_service: ClientService = Depends(Provide[Application.services.client_service]),

    page_limit: int = Depends(Provide[Application.config.CLIENTS_PER_PAGE])

) -> Response:
    """Returns clients per given page."""

    paginated_clients = client_service.get_many(page, page_limit, uid=uid, start_created=start_created,
                                                end_created=end_created, ordering=ordering)

    json_compatible_content = jsonable_encoder(paginated_clients)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.post(
    '/clients',
    responses={
        201: {'model': GetClientSchema, 'description': 'Created item'},
    }
)
@inject
def create_client(

    client_service: ClientService = Depends(Provide[Application.services.client_service]),

    secret_manager: SecretManager = Depends(Provide[Application.managers.secret_manager]),

    api_key: str = Depends(get_api_key)

) -> Response:
    """Creates new client."""

    raw_secret = secrets.token_hex(32)
    hashed_secret = secret_manager.get_hash(raw_secret)
    client_schema = CreateClientSchema(uid=uuid.uuid4().hex, secret=hashed_secret)

    client = client_service.create(client_schema)

    client.secret = raw_secret

    json_compatible_content = jsonable_encoder(client)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_compatible_content)


@router.get(
    '/clients/{client_id}',
    responses={
        200: {'model': GetClientSchema, 'description': 'Item requested by ID'},
        404: {'model': HTTPExceptionSchema, 'description': 'Item was not found'},
    }
)
@inject
def get_client(

    client_id: int,

    client_service: ClientService = Depends(Provide[Application.services.client_service])

) -> Response:
    """Returns client with passed ID."""

    try:
        client = client_service.get_one_by_id(client_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client with ID "{client_id}" was not found')
    else:
        json_compatible_content = jsonable_encoder(client)
        return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.put(
    '/clients/{client_id}',
    responses={
        201: {'model': GetClientSchema, 'description': 'Created item'},
    }
)
@inject
def update_client(

    client_id: int,

    client_service: ClientService = Depends(Provide[Application.services.client_service]),

    secret_manager: SecretManager = Depends(Provide[Application.managers.secret_manager]),

    api_key: str = Depends(get_api_key)

) -> Response:
    """Updates client's secret."""

    raw_secret = secrets.token_hex(32)
    hashed_secret = secret_manager.get_hash(raw_secret)

    try:
        client = client_service.update(client_id, hashed_secret)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client with ID "{client_id}" was not found')
    else:
        client.secret = raw_secret

        json_compatible_content = jsonable_encoder(client)
        return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.post(  # DELETE can be blocked by proxy server
    '/clients/delete',
    responses={
        207: {'model': StatusesSchema, 'description': 'List of deletion statuses for each processed object.'},
    }
)
@inject
def delete(

    ids_schema: IdsSchema,

    client_service: ClientService = Depends(Provide[Application.services.client_service]),

    api_key: str = Depends(get_api_key)

) -> Response:
    """Deletes clients with passed IDs."""

    results = client_service.delete(ids_schema)

    json_compatible_content = jsonable_encoder(results)
    return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=json_compatible_content)
