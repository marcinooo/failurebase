"""Unit of Work module."""

from abc import ABCMeta, abstractmethod
from typing import Callable, Any


class BaseUnitOfWork(metaclass=ABCMeta):
    """UoW to manage database repositories."""

    @abstractmethod
    def __init__(self, session_factory: Callable) -> None:
        self.session_factory = session_factory

    @abstractmethod
    def __enter__(self) -> 'BaseUnitOfWork':
        """Creates current session."""

        self.session = self.session_factory()

        return self

    def commit(self) -> None:
        """Commits current session."""

        self.session.commit()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Closes current session."""

        self.session.rollback()
        self.session.close()
