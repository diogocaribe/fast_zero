from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_ola_mundo():
    # Fases do test
    client = TestClient(app)  # Arragen (organização)
    response = client.get('/')  # Act (Ação)
    assert response.status_code == HTTPStatus.OK  # Afirmação (garantir)
    assert response.json() == {'message': 'Olá mundo'}
