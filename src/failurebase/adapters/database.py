"""Database module."""

import logging
from sqlalchemy import create_engine, orm

from .models import Base


logger = logging.getLogger(__name__)


class Database:

    def __init__(self, db_url: str) -> None:

        self._engine = create_engine(db_url)

        self.session_factory = orm.scoped_session(
            orm.sessionmaker(
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:

        Base.metadata.create_all(self._engine)
