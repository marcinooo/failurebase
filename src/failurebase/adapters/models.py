"""Models module."""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base model class."""


class ApiKey(Base):
    """Api key allows to perform sensitive actions like object deletions..."""

    __tablename__ = 'apikeys'

    id: Mapped[int] = mapped_column(primary_key=True)

    encrypted_value: Mapped[str] = mapped_column(String(3000))
    created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f'<ApiKey(id={self.id})>'


class Client(Base):
    """Client sends events from test cases."""

    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)

    uid: Mapped[str] = mapped_column(String(32), unique=True)
    secret: Mapped[str] = mapped_column(String(64))
    created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    events: Mapped[list['Event']] = relationship(back_populates='client', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Client(id={self.id})>'


class Test(Base):
    """Tests represents executed test case."""

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
    """Represents single failure."""

    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)

    message: Mapped[str] = mapped_column(String(2000))
    traceback: Mapped[str] = mapped_column(String(3000))
    client_timestamp: Mapped[datetime] = mapped_column(DateTime())
    server_timestamp: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    test: Mapped['Test'] = relationship(back_populates='events')
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    client: Mapped['Client'] = relationship(back_populates='events')

    def __repr__(self):
        return f'<Event(id={self.id})>'
