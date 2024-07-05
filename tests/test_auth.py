from http import HTTPStatus


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


def test_get_token_invalid_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.wrong_email, 'password': user.clean_password},
    )
    # assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_invalid_pwd(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.wrong_pwd},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
