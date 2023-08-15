"""ApiKey service module."""

from typing import Type

from failurebase.services.base.service import BaseService
from failurebase.services.api_key.uow import ApiKeyUnitOfWork
from failurebase.adapters.repositories.api_key import ApiKeyRepository
from failurebase.adapters.models import ApiKey
from failurebase.schemas.api_key import GetApiKeySchema, CreateApiKeySchema
from failurebase.schemas.common import PaginationSchema


class ApiKeyService(BaseService[ApiKeyUnitOfWork, CreateApiKeySchema, GetApiKeySchema]):
    """Service to manage ApiKey objects."""

    def __init__(self, uow: ApiKeyUnitOfWork) -> None:
        self.uow = uow

    @property
    def _service_repository(self) -> Type[ApiKeyRepository]:
        return self.uow.api_key_repository

    @property
    def _get_schema(self) -> Type[GetApiKeySchema]:
        return GetApiKeySchema

    def get_many(self, page_number: int = 0, page_limit: int = 1000, *args, **kwargs) -> PaginationSchema:
        """Returns many Clients which are filtered by passed parameters."""

        return super().get_many(page_number, page_limit, **kwargs)

    def create(self, obj_schema: Type[CreateApiKeySchema], *args, **kwargs) -> GetApiKeySchema:
        """Creates new object if it does not exist in database."""

        with self.uow as uow:

            api_key_obj = ApiKey(encrypted_value=obj_schema.value, created=obj_schema.created)
            uow.api_key_repository.create(api_key_obj)

            uow.commit()

            api_key_schema = GetApiKeySchema.from_orm(api_key_obj)

        return api_key_schema
