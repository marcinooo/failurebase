"""Event service module."""

from logging import getLogger
from typing import Type
from datetime import datetime
from fastapi import status

from failurebase.services.base.service import BaseService
from failurebase.services.event.uow import EventUnitOfWork
from failurebase.adapters.repositories.event import EventRepository
from failurebase.adapters.models import Event, Test
from failurebase.adapters.exceptions import NotFoundError
from failurebase.schemas.event import GetEventSchema, CreateEventSchema
from failurebase.schemas.client import GetClientSchema
from failurebase.schemas.common import IdsSchema, StatusesSchema


logger = getLogger(__name__)


class EventService(BaseService[EventUnitOfWork, CreateEventSchema, GetEventSchema]):
    """Service to manage Event objects."""

    def __init__(self, uow: EventUnitOfWork) -> None:
        self.uow = uow

    @property
    def _service_repository(self) -> Type[EventRepository]:
        return self.uow.event_repository

    @property
    def _get_schema(self) -> Type[GetEventSchema]:
        return GetEventSchema

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
                logger.info('%s was created', test_obj)
            else:
                test_obj.file = event_schema.test.file
                test_obj.marks = event_schema.test.serialized_marks
                test_obj.total_events_count += 1
                logger.info('%s was updated', test_obj)

            client_obj = uow.client_repository.get_by_uid(client_schema.uid)
            event_obj = Event(message=event_schema.message, traceback=event_schema.traceback, test=test_obj,
                              client_timestamp=event_schema.deserialized_timestamp, server_timestamp=datetime.now(),
                              client=client_obj)

            uow.event_repository.create(event_obj)

            uow.commit()

            logger.info('%s was created', event_obj)

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

                logger.info('Deletion statuses: %s', str(statuses))
                logger.info('Number of events for %s: %s', event.test, event.test.total_events_count)

        return StatusesSchema(statuses=statuses)
