"""Client Unit of Work module."""

from typing import Callable, Type

from failurebase.services.base.uow import BaseUnitOfWork
from failurebase.adapters.repositories.client import ClientRepository


class ClientUnitOfWork(BaseUnitOfWork):
    """UoW to manage database repositories under Client service."""

    def __init__(self,
                 session_factory: Callable,
                 client_repository_cls: Type[ClientRepository]) -> None:
        super().__init__(session_factory)

        self.client_repository_cls = client_repository_cls

    def __enter__(self) -> 'ClientUnitOfWork':
        """Creates Client repository."""

        super().__enter__()

        self.client_repository = self.client_repository_cls(self.session)

        return self
