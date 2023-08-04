"""Test service module."""

from fastapi import status

from failurebase.services.uow import DatabaseUnitOfWork
from failurebase.schemas.test import GetTestSchema
from failurebase.schemas.common import IdsSchema, StatusesSchema, PaginationSchema
from failurebase.adapters.exceptions import NotFoundError


class TestService:
    """Service to manage Test objects."""

    def __init__(self, uow: DatabaseUnitOfWork) -> None:
        self.uow = uow

    def get_many(self, page_number: int, page_limit: int, uid: str | None, file: str | None,
                 marks: str | None, ordering: str | None) -> list[GetTestSchema]:
        """Returns many Tests which are paginated."""

        with self.uow as uow:

            paginated_tests = uow.test_repository.get_many(
                page_number=page_number, page_limit=page_limit, uid=uid, file=file, marks=marks, ordering=ordering
            )

            event_schemas = [GetTestSchema.from_orm(test) for test in paginated_tests.chunk]
            pagination_schema = PaginationSchema(
                items=event_schemas, count=paginated_tests.count, page_number=paginated_tests.page_number,
                page_limit=paginated_tests.page_limit, next_page=paginated_tests.next_page,
                prev_page=paginated_tests.prev_page
            )

        return pagination_schema

    def get_one_by_id(self, test_id: str) -> GetTestSchema:
        """Returns single Test by id."""

        with self.uow as uow:
            test = uow.test_repository.get_by_id(test_id)
            test_schema = GetTestSchema.from_orm(test)

        return test_schema

    def delete(self, ids_schema: IdsSchema):
        """Deletes Tests by passed ids."""

        statuses = []

        if ids_schema.ids:

            with self.uow as uow:

                for id_ in ids_schema.ids:
                    try:
                        uow.test_repository.delete_by_id(id_)
                    except NotFoundError:
                        statuses.append({'id': id_, 'status': status.HTTP_404_NOT_FOUND})
                    else:
                        statuses.append({'id': id_, 'status': status.HTTP_200_OK})

                uow.commit()

        return StatusesSchema(statuses=statuses)
