"""ApiKey service module."""

from datetime import datetime
from fastapi import status

from failurebase.services.uow import DatabaseUnitOfWork
from failurebase.adapters.models import ApiKey
from failurebase.adapters.exceptions import NotFoundError
from failurebase.schemas.api_key import GetApiKeySchema, CreateApiKeySchema
from failurebase.schemas.common import PaginationSchema, IdsSchema, StatusesSchema


class ApiKeyService:
    """Service to manage ApiKey objects."""

    def __init__(self, uow: DatabaseUnitOfWork) -> None:
        self.uow = uow

    def get_all(self) -> PaginationSchema:
        """Returns all ApiKeys."""

        page_number = 0
        page_limit = 1000

        with self.uow as uow:

            paginated_api_keys = uow.api_key_repository.get_many(page_number=page_number, page_limit=page_limit)

            api_key_schemas = [GetApiKeySchema.from_orm(api_key) for api_key in paginated_api_keys.chunk]

            pagination_schema = PaginationSchema(
                items=api_key_schemas, count=paginated_api_keys.count, page_number=0,
                page_limit=paginated_api_keys.page_limit, next_page=False, prev_page=False
            )

        return pagination_schema

    # def get_one_by_uid(self, id: str) -> GetApiKeySchema | None:
    #     """Returns single Client by uid."""
    #
    #     with self.uow as uow:
    #         try:
    #             client = uow.client_repository.get_by_uid(uid)
    #         except NotFoundError:
    #             client_schema = None
    #         else:
    #             client_schema = GetClientSchema.from_orm(client)
    #
    #     return client_schema

    def create(self, api_key_schema: CreateApiKeySchema) -> GetApiKeySchema:
        """Creates new Client."""

        with self.uow as uow:

            api_key_obj = ApiKey(encrypted_value=api_key_schema.value, created=api_key_schema.created)
            uow.api_key_repository.create(api_key_obj)

            uow.commit()

            api_key_schema = GetApiKeySchema.from_orm(api_key_obj)

        return api_key_schema

    # def delete(self, ids_schema: IdsSchema):
    #     """Deletes Clients by passed ids."""
    #
    #     statuses = []
    #
    #     if ids_schema.ids:
    #
    #         with self.uow as uow:
    #
    #             for id_ in ids_schema.ids:
    #                 try:
    #                     uow.client_repository.delete_by_id(id_)
    #                 except NotFoundError:
    #                     statuses.append({'id': id_, 'status': status.HTTP_404_NOT_FOUND})
    #                 else:
    #                     statuses.append({'id': id_, 'status': status.HTTP_200_OK})
    #
    #             uow.commit()
    #
    #     return StatusesSchema(statuses=statuses)
