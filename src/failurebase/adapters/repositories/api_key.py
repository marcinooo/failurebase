"""Client repository module."""

from .base import AbstractRepository, PaginationList
from ..models import ApiKey
from ..exceptions import NotFoundError


class ApiKeyRepository(AbstractRepository):
    """Repository to manage `ApiKey` model."""

    def get_many(self, page_number: int, page_limit: int, **kwargs) -> PaginationList:
        """Returns many paginated objects."""

        query = self.session.query(ApiKey)

        offset = page_number * page_limit

        count = query.count()

        query = query.offset(offset).limit(page_limit)
        chunk = query.all()
        next_page = offset + page_limit < count
        prev_page = page_number > 0

        return PaginationList(chunk, count, page_number, page_limit, next_page, prev_page)

    def get_by_id(self, api_key_id: int) -> ApiKey:
        """Returns single object with given id."""

        api_key = self.session.get(ApiKey, api_key_id)
        if api_key is None:
            raise NotFoundError(f'ApiKey with id = "{api_key_id}" does not exist.')

        return api_key

    def create(self, api_key: ApiKey) -> None:
        """Creates single object in current session."""

        self.session.add(api_key)

    def delete_by_id(self, api_key_id: int) -> ApiKey:
        """Deletes single object with given id."""

        api_key = self.session.query(ApiKey).filter(ApiKey.id == api_key_id).first()
        if api_key is None:
            raise NotFoundError(f'ApiKey with id = "{api_key_id}" does not exist.')

        self.session.delete(api_key)

        return api_key
