"""Base repository module."""

from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Type
from dataclasses import dataclass
from sqlalchemy.orm import Session

from ..exceptions import NotFoundError


MODEL = TypeVar("MODEL")


@dataclass
class PaginationList:
    chunk: list
    count: int
    page_number: int
    page_limit: int
    next_page: bool
    prev_page: bool


class AbstractRepository(Generic[MODEL], metaclass=ABCMeta):
    """Repository interface."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @property
    @abstractmethod
    def _model(self) -> Type[MODEL]:
        """Returns database Model"""

    @abstractmethod
    def _order_clause(self, **kwargs) -> tuple:
        """Returns order clause to put it in `order_by` method."""

    @abstractmethod
    def _filters(self, **kwargs) -> tuple:
        """Returns filter list to put it in `filter` method."""

    def get_many(self, page_number: int, page_limit: int, **kwargs) -> PaginationList:
        """Returns many paginated objects."""

        query = self.session.query(self._model)

        filters, filters_related_objs = self._filters(**kwargs)
        order_clause, order_clause_related_objs = self._order_clause(**kwargs)

        for related_obj in filters_related_objs.union(order_clause_related_objs):
            query = query.join(related_obj)

        if filters:
            query = query.filter(*filters)

        offset = page_number * page_limit

        query = query.order_by(order_clause)
        count = query.count()

        query = query.offset(offset).limit(page_limit)
        chunk = query.all()
        next_page = offset + page_limit < count
        prev_page = page_number > 0

        return PaginationList(chunk, count, page_number, page_limit, next_page, prev_page)

    def get_by_id(self, obj_id: int) -> MODEL:
        """Returns single object with given id."""

        obj = self.session.get(self._model, obj_id)
        if obj is None:
            raise NotFoundError(f'{self._model.__class__.__name__} with id = "{obj_id}" does not exist.')

        return obj

    def create(self, obj: MODEL) -> None:
        """Creates single object."""

        self.session.add(obj)

    def delete_by_id(self, obj_id: int) -> MODEL:
        """Deletes single object with given id."""

        obj = self.session.query(self._model).filter(self._model.id == obj_id).first()
        if obj is None:
            raise NotFoundError(f'{self._model.__class__.__name__} with id = "{obj_id}" does not exist.')

        self.session.delete(obj)

        return obj
