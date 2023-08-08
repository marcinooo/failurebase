"""Test Unit of Work module."""

from typing import Callable, Type

from failurebase.services.base.uow import BaseUnitOfWork
from failurebase.adapters.repositories.test import TestRepository


class TestUnitOfWork(BaseUnitOfWork):
    """UoW to manage database repositories under Test service."""

    def __init__(self,
                 session_factory: Callable,
                 test_repository_cls: Type[TestRepository]) -> None:

        super().__init__(session_factory)

        self.test_repository_cls = test_repository_cls

    def __enter__(self) -> 'TestUnitOfWork':
        """Creates Test repository."""

        super().__enter__()

        self.test_repository = self.test_repository_cls(self.session)

        return self
