"""Client service module."""

from typing import Type

from failurebase.services.base.service import BaseService
from failurebase.services.client.uow import ClientUnitOfWork
from failurebase.adapters.repositories.client import ClientRepository
from failurebase.adapters.models import Client
from failurebase.adapters.exceptions import NotFoundError
from failurebase.schemas.client import GetClientSchema, CreateClientSchema


class ClientService(BaseService[ClientUnitOfWork, CreateClientSchema, GetClientSchema]):
    """Service to manage Client objects."""

    def __init__(self, uow: ClientUnitOfWork) -> None:
        self.uow = uow

    @property
    def _service_repository(self) -> Type[ClientRepository]:
        return self.uow.client_repository

    @property
    def _get_schema(self) -> Type[GetClientSchema]:
        return GetClientSchema

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

    def create(self, obj_schema: Type[CreateClientSchema], *args, **kwargs) -> GetClientSchema:
        """Creates new object if it does not exist in database."""

        with self.uow as uow:
            client_obj = Client(uid=obj_schema.uid, secret=obj_schema.secret)
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
