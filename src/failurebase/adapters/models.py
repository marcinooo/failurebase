"""Models module."""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base model class."""


class Test(Base):

    __tablename__ = 'tests'
    __test__ = False

    id: Mapped[int] = mapped_column(primary_key=True)

    uid: Mapped[str] = mapped_column(String(2000), unique=True)
    marks: Mapped[str] = mapped_column(String(2000))
    file: Mapped[str] = mapped_column(String(1000))
    total_events_count: Mapped[int] = mapped_column(Integer())
    events: Mapped[list['Event']] = relationship(back_populates='test', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Test(id={self.id})>'


class Event(Base):

    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)

    message: Mapped[str] = mapped_column(String(2000))
    traceback: Mapped[str] = mapped_column(String(3000))
    client_timestamp: Mapped[datetime] = mapped_column(DateTime())
    server_timestamp: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    test: Mapped['Test'] = relationship(back_populates='events')

    def __repr__(self):
        return f'<Event(id={self.id})>'
