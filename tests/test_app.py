from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_ola_mundo():
    # Fases do test
    client = TestClient(app)  # Arragen (organização)
    response = client.get('/')  # Act (Ação)
    # Afirmação (garantir)
    assert response.json() == {'message': 'Olá mundo'}
