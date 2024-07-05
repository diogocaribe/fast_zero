from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    user_test = {  # UserSchema
        'username': 'usernameteste',
        'email': 'emailteste@test.com',
        'password': 'password',
    }

    user_response = {
        'id': 1,
        'username': 'usernameteste',
        'email': 'emailteste@test.com',
    }
    response = client.post('/users/', json=user_test)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_response


def test_create_user_already_exist(client, user):
    user_test = {  # UserSchema
        'username': 'alice',
        'email': 'alice@teste.com',
        'password': 'password',
    }
    response = client.post('/users/', json=user_test)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exist(client, user):
    user_test = {  # UserSchema
        'username': 'alice_',
        'email': 'alice@teste.com',
        'password': '123',
    }
    response = client.post('/users/', json=user_test)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    lista_users = {'users': []}
    assert response.status_code == HTTPStatus.OK
    assert response.json() == lista_users


def test_read_users_with_user(client, user):
    response = client.get('/users/')
    # assert response.status_code() == HTTPStatus.OK
    user_schema = UserPublic.model_validate(user).model_dump()
    assert response.json() == {
        'users': [
            # UserPublic
            user_schema
        ]
    }


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_id_not_found(client, user, token):
    client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123',
            'username': 'alice',
            'email': 'alice@teste.com',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_diff_from_logged(client, user, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_get_user_id(client, user):
    user_response = {
        'id': 1,
        'username': 'alice',
        'email': 'alice@teste.com',
    }

    response = client.get('/users/1')

    assert response.json() == user_response


def test_get_user_id_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
