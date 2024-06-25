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
    response = client.post('/user/', json=user_test)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_response


def test_read_users(client):
    response = client.get('/users/')
    lista_users = {'users': [
        {
            'id': 1,
            'username': 'usernameteste',
            'email': 'emailteste@test.com',
        }
    ]}
    assert response.status_code == HTTPStatus.OK
    assert response.json() == lista_users
