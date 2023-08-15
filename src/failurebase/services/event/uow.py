"""Event Unit of Work module."""

from typing import Callable, Type

from failurebase.services.base.uow import BaseUnitOfWork
from failurebase.adapters.repositories.event import EventRepository
from failurebase.adapters.repositories.test import TestRepository
from failurebase.adapters.repositories.client import ClientRepository


class EventUnitOfWork(BaseUnitOfWork):
    """UoW to manage database repositories under Event service."""

    def __init__(self,
                 session_factory: Callable,
                 event_repository_cls: Type[EventRepository],
                 test_repository_cls: Type[TestRepository],
                 client_repository_cls: Type[ClientRepository]) -> None:

        super().__init__(session_factory)

        self.event_repository_cls = event_repository_cls
        self.test_repository_cls = test_repository_cls
        self.client_repository_cls = client_repository_cls

    def __enter__(self) -> 'EventUnitOfWork':
        """Creates Event, Test and Client repositories."""

        super().__enter__()

        self.event_repository = self.event_repository_cls(self.session)
        self.test_repository = self.test_repository_cls(self.session)
        self.client_repository = self.client_repository_cls(self.session)

        return self
