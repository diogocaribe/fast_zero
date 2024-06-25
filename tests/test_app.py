from http import HTTPStatus


def test_read_root_deve_retornar_ok_ola_mundo(client):
    # Fases do test
    response = client.get('/')  # Act (Ação)
    # Afirmação (garantir)
    assert response.json() == {'message': 'Olá mundo'}


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


def test_read_users(client):
    response = client.get('/users/')
    lista_users = {
        'users': [
            {
                'id': 1,
                'username': 'usernameteste',
                'email': 'emailteste@test.com',
            }
        ]
    }
    assert response.status_code == HTTPStatus.OK
    assert response.json() == lista_users


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': '123',
            'username': 'nematest',
            'email': 'teste@teste.com',
            'id': 1,
        },
    )

    # assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'username': 'nematest',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_update_user_id_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'password': '123',
            'username': 'nematest',
            'email': 'teste@teste.com',
            'id': 1,
        },
    )

    # assert response.status_code == HTTPStatus.OK

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_user_id_not_found(client):
    client.post(
        '/users/1',
        json={'password': '123', 'username': 'nematest', 'email': 'teste@teste.com'},
    )

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_id(client):
    user_test = {  # UserSchema
        'username': 'usernameteste',
        'email': 'emailteste@test.com',
        'password': 'password',
    }

    user_response = {
        'id': 2,
        'username': 'usernameteste',
        'email': 'emailteste@test.com',
    }
    client.post('/users/', json=user_test)
    client.post('/users/', json=user_test)
    response = client.get('/users/2')

    assert response.json() == user_response
