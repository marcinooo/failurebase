"""Client repository module."""

from typing import Type

from .base import AbstractRepository
from ..models import Client
from ..exceptions import NotFoundError


class ClientRepository(AbstractRepository[Client]):
    """Repository to manage `Client` model."""

    POSSIBLE_ORDER_CLAUSES = {
        'uid': Client.uid.asc(),
        '-uid': Client.uid.desc(),
        'created': Client.created.asc(),
        '-created': Client.created.desc()
    }

    @property
    def _model(self) -> Type[Client]:
        return Client

    def _filters(self, **kwargs):
        filters = []
        related_objs = set()

        uid = kwargs.get('uid')
        if uid is not None:
            filters.append(Client.uid.ilike(f'%{uid}%'))

        start_created = kwargs.get('start_created')
        if start_created is not None:
            filters.append(start_created <= Client.created)

        end_created = kwargs.get('end_created')
        if end_created is not None:
            filters.append(Client.created <= end_created)

        return filters, related_objs

    def _order_clause(self, **kwargs):
        order_clause = Client.created.desc()
        related_objs = set()
        ordering = kwargs.get('ordering')
        if ordering is not None:
            order_clause = self.POSSIBLE_ORDER_CLAUSES[ordering]
        return order_clause, related_objs

    def get_by_uid(self, uid: int) -> Client:
        """Returns single object with given uid."""

        client = self.session.query(Client).filter(Client.uid == uid).first()
        if client is None:
            raise NotFoundError(f'Client with uid = "{uid}" does not exist.')

        return client
