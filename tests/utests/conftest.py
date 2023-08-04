import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from jose import JWTError, jwt

from .data import events, tests, clients, API_KEY

from failurebase.application import create_app
from failurebase.adapters.models import Test, Event, Client, ApiKey


@pytest.fixture(scope='session')
def client():

    app = create_app()

    client = TestClient(app)

    yield client


@pytest.fixture(scope='session')
def config(client):

    yield client.app.container.config()


@pytest.fixture()
def database_session(client, config):

    database_uri = config['DATABASE_URI']
    secret_key = config['SECRET_KEY']

    engine = create_engine(database_uri)

    with Session(engine) as session:

        session.query(Event).delete()
        session.query(Test).delete()
        session.query(Client).delete()
        session.query(ApiKey).delete()

        api_key = ApiKey(encrypted_value=encrypted_value(API_KEY, secret_key))

        session.add(api_key)

        for test_data, event_data, client_data in zip(tests.values(), events.values(), clients.values()):
            new_client_data = client_data.copy()
            new_client_data['secret'] = hash_value(client_data['secret'])
            client_obj = Client(**new_client_data)
            test_obj = Test(**test_data)
            event_obj = Event(**event_data, test=test_obj, client=client_obj)
            session.add(event_obj)

        session.commit()

        yield session


@pytest.fixture()
def jwt_token_factory(config):
    secret_key = config['SECRET_KEY']

    return lambda client_uid: create_jwt_token(data={"sub": client_uid},
                                               expires_delta=timedelta(2),
                                               secret_key=secret_key)


def create_jwt_token(data: dict, expires_delta: timedelta, secret_key: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm='HS256')
    return encoded_jwt


def encrypted_value(data, secret_key):
    fernet = Fernet(secret_key.encode('utf-8'))
    return fernet.encrypt(data.encode('utf-8')).decode('utf-8')


def hash_value(data):
    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return crypt_context.hash(data)
