"""Repository interface module."""

from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass
from sqlalchemy.orm import Session


@dataclass
class PaginationList:
    chunk: list
    count: int
    page_number: int
    page_limit: int
    next_page: bool
    prev_page: bool


class AbstractRepository(ABC):
    """Repository interface."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def get_many(self, page_number: int, page_limit: int, **kwargs) -> list[Any]:
        """Signatures of method to return many paginated objects."""

        raise NotImplemented

    # TODO: add other methods
