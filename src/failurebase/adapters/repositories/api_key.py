"""ApiKey repository module."""

from typing import Type

from .base import AbstractRepository
from ..models import ApiKey


class ApiKeyRepository(AbstractRepository[ApiKey]):
    """Repository to manage `ApiKey` model."""

    @property
    def _model(self) -> Type[ApiKey]:
        return ApiKey

    def _filters(self, **kwargs):
        filters = []
        related_objs = set()
        return filters, related_objs

    def _order_clause(self, **kwargs):
        order_clause = ApiKey.created.desc()
        related_objs = set()
        return order_clause, related_objs
