"""Test handlers module."""

from logging import getLogger
from typing import Annotated
from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from failurebase.endpoints.test.validators import TestsOrder
from failurebase.endpoints.auth.utils import get_api_key
from failurebase.services.test.service import TestService
from failurebase.containers import Application
from failurebase.schemas.test import GetTestSchema
from failurebase.schemas.common import HTTPExceptionSchema, StatusesSchema, IdsSchema, PaginationSchema
from failurebase.adapters.exceptions import NotFoundError


logger = getLogger(__name__)

router = APIRouter()


@router.get(
    '/tests',
    responses={
        200: {'model': PaginationSchema, 'description': 'Requested items'}
    }
)
@inject
def get_tests(

    page: Annotated[
        int, Query(title='Page number', description='The list of returned objects is broken down into smaller '
                                                    'chunks that can be retrieved via the page index.')
    ] = 0,

    uid: Annotated[
        str | None, Query(title='Test UID', description='Unique identifier of test.', max_length=2000)
    ] = None,

    mark: Annotated[
        list[str] | None, Query(title='Test mark', description='Mark of test.', max_length=2000)
    ] = None,

    file: Annotated[
        str | None, Query(title='Test File Path', description='File path of test.', max_length=1000)
    ] = None,

    ordering: Annotated[
        str | None, Query(title='Order By Given Column',
                          description='Tests will be sorted by given test property.',
                          regex=f'^({"|".join(o.value for o in TestsOrder)})$')
    ] = None,

    test_service: TestService = Depends(Provide[Application.services.test_service]),

    page_limit: int = Depends(Provide[Application.config.TESTS_PER_PAGE])

) -> Response:
    """Returns tests per given page."""

    paginated_tests = test_service.get_many(page, page_limit, uid=uid, file=file, marks=mark, ordering=ordering)

    json_compatible_content = jsonable_encoder(paginated_tests)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.get(
    '/tests/{test_id}',
    responses={
        200: {'model': GetTestSchema, 'description': 'Item requested by ID'},
        404: {'model': HTTPExceptionSchema, 'description': 'Item was not found'},
    }
)
@inject
def get_test(

    test_id: int,

    test_service: TestService = Depends(Provide[Application.services.test_service]),

) -> Response:
    """Returns test with passed ID."""

    try:
        test = test_service.get_one_by_id(test_id)
    except NotFoundError:
        logger.error('Test with id %s was not found', test_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Test with id "{test_id}" was not found')
    else:
        json_compatible_content = jsonable_encoder(test)
        return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_content)


@router.post(  # DELETE can be blocked by proxy server
    '/tests/delete',
    responses={
        207: {'model': StatusesSchema, 'description': 'List of deletion statuses for each object ID.'},
    }
)
@inject
def delete(

    ids_schema: IdsSchema,

    event_service: TestService = Depends(Provide[Application.services.test_service]),

    api_key: str = Depends(get_api_key)

) -> Response:
    """Deletes tests with passed IDs."""

    results = event_service.delete(ids_schema)

    json_compatible_content = jsonable_encoder(results)
    return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=json_compatible_content)
