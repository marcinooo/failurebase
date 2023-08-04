"""Unit of Work module."""

from typing import Callable, Type, Any

from ..adapters.repositories.event import EventRepository
from ..adapters.repositories.test import TestRepository
from ..adapters.repositories.client import ClientRepository
from ..adapters.repositories.api_key import ApiKeyRepository


class DatabaseUnitOfWork:
    """UoW to manage database repositories repositories."""

    def __init__(self,
                 session_factory: Callable,
                 event_repository_cls: Type[EventRepository],
                 test_repository_cls: Type[TestRepository],
                 client_repository_cls: Type[ClientRepository],
                 api_key_repository_cls: Type[ApiKeyRepository]) -> None:

        self.session_factory = session_factory
        self.event_repository_cls = event_repository_cls
        self.test_repository_cls = test_repository_cls
        self.client_repository_cls = client_repository_cls
        self.api_key_repository_cls = api_key_repository_cls

    def __enter__(self) -> 'DatabaseUnitOfWork':
        """Creates session, Event, Test, Client and ApiKey repositories."""

        self.session = self.session_factory()
        self.event_repository = self.event_repository_cls(self.session)
        self.test_repository = self.test_repository_cls(self.session)
        self.client_repository = self.client_repository_cls(self.session)
        self.api_key_repository = self.api_key_repository_cls(self.session)

        return self

    def commit(self) -> None:
        """Commits current session."""

        self.session.commit()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Closes current session."""

        self.session.rollback()
        self.session.close()
