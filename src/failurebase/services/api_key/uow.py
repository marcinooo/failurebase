"""ApiKey Unit of Work module."""

from typing import Callable, Type

from failurebase.services.base.uow import BaseUnitOfWork
from failurebase.adapters.repositories.api_key import ApiKeyRepository


class ApiKeyUnitOfWork(BaseUnitOfWork):
    """UoW to manage database repositories under ApiKey service."""

    def __init__(self,
                 session_factory: Callable,
                 api_key_repository_cls: Type[ApiKeyRepository]) -> None:
        super().__init__(session_factory)

        self.api_key_repository_cls = api_key_repository_cls

    def __enter__(self) -> 'ApiKeyUnitOfWork':
        """Creates ApiKey repository."""

        super().__enter__()

        self.api_key_repository = self.api_key_repository_cls(self.session)

        return self
