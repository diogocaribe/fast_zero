from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    decoded = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
    assert decoded['sub'] == data['sub']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_get_token(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': user.clean_password}
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    # Testando se existe o token_type
    assert token['token_type'] == 'Bearer'
    # Testando se existe o access_token
    assert 'access_token' in token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
