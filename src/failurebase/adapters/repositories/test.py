"""Test repository module."""

from .base import AbstractRepository, PaginationList
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

    def get_many(self, page_number: int, page_limit: int, **kwargs) -> PaginationList:
        """Returns many paginated objects."""

        query = self.session.query(Test)
        filters = []
        order_clause = Test.uid.desc()

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

        ordering = kwargs.get('ordering')
        if ordering is not None:
            order_clause = self.POSSIBLE_ORDER_CLAUSES[ordering]

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

    def get_by_id(self, test_id: int) -> Test:
        """Returns single object with given id."""

        test = self.session.get(Test, test_id)
        if test is None:
            raise NotFoundError(f'Test with id = "{test_id}" does not exist.')

        return test

    def get_by_uid(self, uid: int) -> Test:
        """Returns single object with given uid."""

        test = self.session.query(Test).filter(Test.uid == uid).first()
        if test is None:
            raise NotFoundError(f'Test with uid = "{uid}" does not exist.')

        return test

    def delete_by_id(self, test_id: int) -> None:
        """Deletes single object with given id."""

        test = self.session.query(Test).filter(Test.id == test_id).first()
        if test is None:
            raise NotFoundError(f'Test with id = "{test_id}" does not exist.')

        self.session.delete(test)

        return test