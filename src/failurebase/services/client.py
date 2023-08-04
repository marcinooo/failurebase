"""Client service module."""

from datetime import datetime
from fastapi import status

from failurebase.services.uow import DatabaseUnitOfWork
from failurebase.adapters.models import Client
from failurebase.adapters.exceptions import NotFoundError
from failurebase.schemas.client import GetClientSchema, CreateClientSchema
from failurebase.schemas.common import PaginationSchema, IdsSchema, StatusesSchema


class ClientService:
    """Service to manage Client objects."""

    def __init__(self, uow: DatabaseUnitOfWork) -> None:
        self.uow = uow

    def get_many(self, page_number: int, page_limit: int, uid: str | None, start_created: datetime | None,
                 end_created: datetime | None, ordering: str | None) -> PaginationSchema:
        """Returns many Clients which are filtered by passed parameters."""

        with self.uow as uow:

            paginated_clients = uow.client_repository.get_many(
                page_number=page_number, page_limit=page_limit, uid=uid, start_created=start_created,
                end_created=end_created, ordering=ordering
            )

            client_schemas = [GetClientSchema.from_orm(client) for client in paginated_clients.chunk]
            pagination_schema = PaginationSchema(
                items=client_schemas, count=paginated_clients.count, page_number=paginated_clients.page_number,
                page_limit=paginated_clients.page_limit, next_page=paginated_clients.next_page,
                prev_page=paginated_clients.prev_page
            )

        return pagination_schema

    def get_one_by_id(self, client_id: int) -> GetClientSchema:
        """Returns single Client by id."""

        with self.uow as uow:
            client = uow.client_repository.get_by_id(client_id)
            client_schema = GetClientSchema.from_orm(client)

        return client_schema

    def get_one_by_uid(self, uid: str) -> GetClientSchema | None:
        """Returns single Client by uid."""

        with self.uow as uow:
            try:
                client = uow.client_repository.get_by_uid(uid)
            except NotFoundError:
                client_schema = None
            else:
                client_schema = GetClientSchema.from_orm(client)

        return client_schema

    def create(self, client_schema: CreateClientSchema) -> GetClientSchema:
        """Creates new Client."""

        with self.uow as uow:

            client_obj = Client(uid=client_schema.uid, secret=client_schema.secret)
            uow.client_repository.create(client_obj)

            uow.commit()

            client_schema = GetClientSchema.from_orm(client_obj)

        return client_schema

    def update(self, client_id: int, hashed_secret: str) -> GetClientSchema:
        """Updates new Client."""

        with self.uow as uow:
            client = uow.client_repository.get_by_id(client_id)

            client.secret = hashed_secret

            uow.commit()

            client_schema = GetClientSchema.from_orm(client)

        return client_schema

    def delete(self, ids_schema: IdsSchema):
        """Deletes Clients by passed ids."""

        statuses = []

        if ids_schema.ids:

            with self.uow as uow:

                for id_ in ids_schema.ids:
                    try:
                        uow.client_repository.delete_by_id(id_)
                    except NotFoundError:
                        statuses.append({'id': id_, 'status': status.HTTP_404_NOT_FOUND})
                    else:
                        statuses.append({'id': id_, 'status': status.HTTP_200_OK})

                uow.commit()

        return StatusesSchema(statuses=statuses)
