from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_ola_mundo():
    # Fases do test
    client = TestClient(app)  # Arragen (organização)
    response = client.get('/')  # Act (Ação)
    # Afirmação (garantir)
    assert response.json() == {'message': 'Olá mundo'}


def test_create_user():
    # Fases do test
    client = TestClient(app)  # Arragen (organização)
    # Act (Ação)
    # Afirmação (garantir)
    user_test = {
        'username': 'usernameteste',
        'email': 'emailteste@test.com',
        'password': 'password',
    }

    user_response = {
        'id': 1,
        'username': 'usernameteste',
        'email': 'emailteste@test.com',
    }
    response = client.post('/user/', json=user_test)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_response
