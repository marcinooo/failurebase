"""Base service module."""

from logging import getLogger
from typing import Generic, Type, TypeVar
from abc import ABCMeta, abstractmethod
from fastapi import status

from failurebase.adapters.repositories.base import AbstractRepository
from failurebase.adapters.exceptions import NotFoundError
from failurebase.schemas.common import PaginationSchema, IdsSchema, StatusesSchema


logger = getLogger(__name__)


UNIT_OF_WORK = TypeVar("UNIT_OF_WORK")
CREATE_SCHEMA = TypeVar("CREATE_SCHEMA")
GET_SCHEMA = TypeVar("GET_SCHEMA")


class BaseService(Generic[UNIT_OF_WORK, CREATE_SCHEMA, GET_SCHEMA], metaclass=ABCMeta):
    """Service interface."""

    @abstractmethod
    def __init__(self, uow: UNIT_OF_WORK) -> None:
        self.uow = uow

    @property
    @abstractmethod
    def _service_repository(self) -> AbstractRepository:
        ...

    @property
    @abstractmethod
    def _get_schema(self) -> Type[GET_SCHEMA]:
        ...

    @abstractmethod
    def create(self, obj_schema: Type[CREATE_SCHEMA], *args, **kwargs) -> Type[GET_SCHEMA]:
        """Creates new object if it does not exist in database."""

    def get_many(self, page_number: int, page_limit: int, *args, **kwargs) -> PaginationSchema:
        """Returns many object which are filtered by passed parameters."""

        with self.uow:
            paginated_objs = self._service_repository.get_many(page_number=page_number, page_limit=page_limit, **kwargs)

            obj_schemas = [self._get_schema.from_orm(event) for event in paginated_objs.chunk]
            pagination_schema = PaginationSchema(
                items=obj_schemas, count=paginated_objs.count, page_number=paginated_objs.page_number,
                page_limit=paginated_objs.page_limit, next_page=paginated_objs.next_page,
                prev_page=paginated_objs.prev_page
            )

        return pagination_schema

    def get_one_by_id(self, obj_id: int) -> Type[GET_SCHEMA]:
        """Returns single object by id."""

        with self.uow:
            event = self._service_repository.get_by_id(obj_id)
            event_schema = self._get_schema.from_orm(event)

        return event_schema

    def delete(self, ids_schema: IdsSchema) -> StatusesSchema:
        """Deletes object by passed ids."""

        statuses = []

        if ids_schema.ids:

            with self.uow as uow:

                for id_ in ids_schema.ids:
                    try:
                        self._service_repository.delete_by_id(id_)
                    except NotFoundError:
                        statuses.append({'id': id_, 'status': status.HTTP_404_NOT_FOUND})
                    else:
                        statuses.append({'id': id_, 'status': status.HTTP_200_OK})

                uow.commit()

        logger.info('Deletion statuses: %s', str(statuses))

        return StatusesSchema(statuses=statuses)
