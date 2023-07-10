"""Event repository module."""

from .base import AbstractRepository, PaginationList
from ..models import Event, Test
from ..exceptions import NotFoundError


class EventRepository(AbstractRepository):
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

    def get_many(self, page_number: int, page_limit: int, **kwargs) -> PaginationList:
        """Returns many paginated objects."""

        query = self.session.query(Event)
        filters = []
        order_clause = Event.server_timestamp.desc()
        related_object = None

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
            related_object = Event.test

        test_marks = kwargs.get('test_marks')
        if test_marks is not None:
            for mark in test_marks:
                filters.append(Test.marks.contains(mark))
            if related_object is None:
                related_object = Event.test

        test_file = kwargs.get('test_file')
        if test_file is not None:
            filters.append(Test.file.ilike(f'%{test_file}%'))
            if related_object is None:
                related_object = Event.test

        ordering = kwargs.get('ordering')
        if ordering is not None:
            order_clause = self.POSSIBLE_ORDER_CLAUSES[ordering]
            if 'test_' in ordering and related_object is None:
                related_object = Event.test

        if related_object is not None:
            query = query.join(related_object)

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

    def get_by_id(self, event_id: int) -> Event:
        """Returns single object with given id."""

        event = self.session.query(Event).get(event_id)
        if event is None:
            raise NotFoundError(f'Event with id = "{event_id}" does not exist.')

        return event

    def create(self, event: Event) -> None:
        """Creates single object in current session."""

        self.session.add(event)

    def delete_by_id(self, event_id: int) -> None:
        """Deletes single object with given id."""

        event = self.session.query(Event).filter(Event.id == event_id).first()
        if event is None:
            raise NotFoundError(f'Event with id = "{event_id}" does not exist.')

        self.session.delete(event)

        return event
