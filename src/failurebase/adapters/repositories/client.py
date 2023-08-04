"""Client repository module."""

from .base import AbstractRepository, PaginationList
from ..models import Client
from ..exceptions import NotFoundError


class ClientRepository(AbstractRepository):
    """Repository to manage `Client` model."""

    POSSIBLE_ORDER_CLAUSES = {
        'uid': Client.uid.asc(),
        '-uid': Client.uid.desc(),
        'created': Client.created.asc(),
        '-created': Client.created.desc()
    }

    def get_many(self, page_number: int, page_limit: int, **kwargs) -> PaginationList:
        """Returns many paginated objects."""

        query = self.session.query(Client)
        filters = []
        order_clause = Client.created.desc()

        uid = kwargs.get('uid')
        if uid is not None:
            filters.append(Client.uid.ilike(f'%{uid}%'))

        start_created = kwargs.get('start_created')
        if start_created is not None:
            filters.append(start_created <= Client.created)

        end_created = kwargs.get('end_created')
        if end_created is not None:
            filters.append(Client.created <= end_created)

        ordering = kwargs.get('ordering')
        if ordering is not None:
            order_clause = self.POSSIBLE_ORDER_CLAUSES[ordering]

        if filters:
            query = query.filter(*filters)

        offset = page_number * page_limit

        query = query.order_by(order_clause)
        count = query.count()

        query = query.offset(offset).limit(page_limit)
        chunk = query.all()
        next_page = offset + page_limit < count
        prev_page = page_number > 0

        return PaginationList(chunk, count, page_number, page_limit, next_page, prev_page)

    def get_by_id(self, client_id: int) -> Client:
        """Returns single object with given id."""

        client = self.session.get(Client, client_id)
        if client is None:
            raise NotFoundError(f'Client with id = "{client_id}" does not exist.')

        return client

    def get_by_uid(self, uid: int) -> Client:
        """Returns single object with given uid."""

        client = self.session.query(Client).filter(Client.uid == uid).first()
        if client is None:
            raise NotFoundError(f'Client with uid = "{uid}" does not exist.')

        return client

    def create(self, client: Client) -> None:
        """Creates single object in current session."""

        self.session.add(client)

    def delete_by_id(self, client_id: int) -> Client:
        """Deletes single object with given id."""

        client = self.session.query(Client).filter(Client.id == client_id).first()
        if client is None:
            raise NotFoundError(f'Client with id = "{client_id}" does not exist.')

        self.session.delete(client)

        return client
