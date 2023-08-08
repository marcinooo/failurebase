"""Test repository module."""

from typing import Type

from .base import AbstractRepository
from ..models import Test
from ..exceptions import NotFoundError


class TestRepository(AbstractRepository):
    """Repository to manage `Test` model."""

    POSSIBLE_ORDER_CLAUSES = {
        'uid': Test.uid.asc(),
        '-uid': Test.uid.desc(),
        'file': Test.file.asc(),
        '-file': Test.file.desc(),
        'total_events_count': Test.total_events_count.asc(),
        '-total_events_count': Test.total_events_count.desc()
    }

    @property
    def _model(self) -> Type[Test]:
        return Test

    def _filters(self, **kwargs):
        filters = []
        related_objs = set()

        uid = kwargs.get('uid')
        if uid is not None:
            filters.append(Test.uid.ilike(f'%{uid}%'))

        file = kwargs.get('file')
        if file is not None:
            filters.append(Test.file.ilike(f'%{file}%'))

        marks = kwargs.get('marks')
        if marks is not None:
            for mark in marks:
                filters.append(Test.marks.contains(mark))

        return filters, related_objs

    def _order_clause(self, **kwargs):
        order_clause = Test.uid.desc()
        related_objs = set()
        ordering = kwargs.get('ordering')
        if ordering is not None:
            order_clause = self.POSSIBLE_ORDER_CLAUSES[ordering]
        return order_clause, related_objs

    def get_by_uid(self, uid: int) -> Test:
        """Returns single object with given uid."""

        test = self.session.query(Test).filter(Test.uid == uid).first()
        if test is None:
            raise NotFoundError(f'Test with uid = "{uid}" does not exist.')

        return test
