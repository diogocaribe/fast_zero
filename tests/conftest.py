import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # TODO Construir a session para realiazr os testes.
    # Tem de fazer o modelo e que ele esteja visível para create table

    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = '123'
    user = UserFactory(password=get_password_hash(pwd))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch
    # Variaveis criadas para testar security
    user.wrong_email = 'bob1@email.com'
    user.wrong_pwd = '1234'
    return user


@pytest.fixture()
def other_user(session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
