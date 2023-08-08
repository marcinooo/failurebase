"""Event repository module."""

from typing import Type

from .base import AbstractRepository
from ..models import Event, Test


class EventRepository(AbstractRepository[Event]):
    """Repository to manage `Event` model."""

    POSSIBLE_ORDER_CLAUSES = {
        'message': Event.message.asc(),
        '-message': Event.message.desc(),
        'server_timestamp': Event.server_timestamp.asc(),
        '-server_timestamp': Event.server_timestamp.desc(),
        'client_timestamp': Event.client_timestamp.asc(),
        '-client_timestamp': Event.client_timestamp.desc(),
        'test_uid': Test.uid.asc(),
        '-test_uid': Test.uid.desc()
    }

    @property
    def _model(self) -> Type[Event]:
        return Event

    def _filters(self, **kwargs):
        filters = []
        related_objs = set()

        start_server_timestamp = kwargs.get('start_server_timestamp')
        if start_server_timestamp is not None:
            filters.append(start_server_timestamp <= Event.server_timestamp)

        end_server_timestamp = kwargs.get('end_server_timestamp')
        if end_server_timestamp is not None:
            filters.append(Event.server_timestamp <= end_server_timestamp)

        start_client_timestamp = kwargs.get('start_client_timestamp')
        if start_client_timestamp is not None:
            filters.append(start_client_timestamp <= Event.client_timestamp)

        end_client_timestamp = kwargs.get('end_client_timestamp')
        if end_client_timestamp is not None:
            filters.append(Event.client_timestamp <= end_client_timestamp)

        message = kwargs.get('message')
        if message is not None:
            filters.append(Event.message.ilike(f'%{message}%'))

        traceback = kwargs.get('traceback')
        if traceback is not None:
            filters.append(Event.traceback.ilike(f'%{traceback}%'))

        test_uid = kwargs.get('test_uid')
        if test_uid is not None:
            filters.append(Test.uid.ilike(f'%{test_uid}%'))
            related_objs.add(Event.test)

        test_marks = kwargs.get('test_marks')
        if test_marks is not None:
            for mark in test_marks:
                filters.append(Test.marks.contains(mark))
            related_objs.add(Event.test)

        test_file = kwargs.get('test_file')
        if test_file is not None:
            filters.append(Test.file.ilike(f'%{test_file}%'))
            related_objs.add(Event.test)

        return filters, related_objs

    def _order_clause(self, **kwargs):
        order_clause = Event.server_timestamp.desc()
        related_objs = set()
        ordering = kwargs.get('ordering')
        if ordering is not None:
            order_clause = self.POSSIBLE_ORDER_CLAUSES[ordering]
            if 'test_' in ordering:
                related_objs.add(Event.test)
        return order_clause, related_objs
