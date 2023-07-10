import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .data import events, tests

from failurebase import app
from failurebase.adapters.models import Test, Event


@pytest.fixture(scope='session')
def client():

    client = TestClient(app)

    yield client


@pytest.fixture(scope='session')
def config(client):

    yield client.app.container.config()


@pytest.fixture()
def database_session(client, config):

    database_uri = config['DATABASE_URI']

    engine = create_engine(database_uri)

    with Session(engine) as session:

        session.query(Event).delete()
        session.query(Test).delete()

        for test, event in zip(tests.values(), events.values()):
            test_obj = Test(**test)
            event_obj = Event(**event, test=test_obj)
            session.add(event_obj)

        session.commit()

        yield session
