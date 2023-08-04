"""Event service module."""

from datetime import datetime
from fastapi import status

from failurebase.services.uow import DatabaseUnitOfWork
from failurebase.adapters.models import Event, Test
from failurebase.adapters.exceptions import NotFoundError
from failurebase.schemas.event import GetEventSchema, CreateEventSchema
from failurebase.schemas.client import GetClientSchema
from failurebase.schemas.common import PaginationSchema, IdsSchema, StatusesSchema


class EventService:
    """Service to manage Event objects."""

    def __init__(self, uow: DatabaseUnitOfWork) -> None:
        self.uow = uow

    def get_one(self, event_id: int) -> GetEventSchema:
        """Returns single Event by id."""

        with self.uow as uow:
            event = uow.event_repository.get_by_id(event_id)
            event_schema = GetEventSchema.from_orm(event)

        return event_schema

    def get_many(self, page_number: int, page_limit: int, start_server_timestamp: datetime | None,
                 end_server_timestamp: datetime | None, start_client_timestamp: datetime | None,
                 end_client_timestamp: datetime | None, message: str | None, traceback: str | None,
                 test_uid: str | None, test_marks: list[str] | None, test_file: str | None,
                 ordering: str | None) -> PaginationSchema:
        """Returns many Events which are filtered by passed parameters."""

        with self.uow as uow:

            paginated_events = uow.event_repository.get_many(
                page_number=page_number, page_limit=page_limit, start_server_timestamp=start_server_timestamp,
                end_server_timestamp=end_server_timestamp, start_client_timestamp=start_client_timestamp,
                end_client_timestamp=end_client_timestamp, message=message, traceback=traceback, test_uid=test_uid,
                test_marks=test_marks, test_file=test_file, ordering=ordering
            )

            event_schemas = [GetEventSchema.from_orm(event) for event in paginated_events.chunk]
            pagination_schema = PaginationSchema(
                items=event_schemas, count=paginated_events.count, page_number=paginated_events.page_number,
                page_limit=paginated_events.page_limit, next_page=paginated_events.next_page,
                prev_page=paginated_events.prev_page
            )

        return pagination_schema

    def create(self, event_schema: CreateEventSchema, client_schema: GetClientSchema) -> GetEventSchema:
        """Creates new Event and Test if it does not exist in database."""

        with self.uow as uow:

            try:
                test_obj = uow.test_repository.get_by_uid(event_schema.test.uid)
            except NotFoundError:
                test_obj = None

            if test_obj is None:
                test_obj = Test(uid=event_schema.test.uid, file=event_schema.test.file,
                                marks=event_schema.test.serialized_marks, total_events_count=1)
            else:
                test_obj.file = event_schema.test.file
                test_obj.marks = event_schema.test.serialized_marks
                test_obj.total_events_count += 1

            client_obj = uow.client_repository.get_by_uid(client_schema.uid)
            event_obj = Event(message=event_schema.message, traceback=event_schema.traceback, test=test_obj,
                              client_timestamp=event_schema.deserialized_timestamp, server_timestamp=datetime.now(),
                              client=client_obj)

            uow.event_repository.create(event_obj)

            uow.commit()

            event_schema = GetEventSchema.from_orm(event_obj)

        return event_schema

    def delete(self, ids_schema: IdsSchema):
        """Deletes Events by passed ids."""

        statuses = []

        if ids_schema.ids:

            with self.uow as uow:

                for id_ in ids_schema.ids:
                    try:
                        event = uow.event_repository.delete_by_id(id_)
                    except NotFoundError:
                        statuses.append({'id': id_, 'status': status.HTTP_404_NOT_FOUND})
                    else:
                        event.test.total_events_count -= 1
                        statuses.append({'id': id_, 'status': status.HTTP_200_OK})

                uow.commit()

        return StatusesSchema(statuses=statuses)
