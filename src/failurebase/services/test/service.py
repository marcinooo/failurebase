"""Test service module."""

from typing import Type

from failurebase.services.base.service import BaseService
from failurebase.services.test.uow import TestUnitOfWork
from failurebase.schemas.test import GetTestSchema, CreateTestSchema
from failurebase.adapters.repositories.test import TestRepository


class TestService(BaseService[TestUnitOfWork, CreateTestSchema, GetTestSchema]):
    """Service to manage Test objects."""

    def __init__(self, uow: TestUnitOfWork) -> None:
        self.uow = uow

    @property
    def _service_repository(self) -> Type[TestRepository]:
        return self.uow.test_repository

    @property
    def _get_schema(self) -> Type[GetTestSchema]:
        return GetTestSchema

    def create(self, obj_schema: Type[CreateTestSchema], *args, **kwargs) -> GetTestSchema:

        raise NotImplementedError
