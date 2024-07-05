def test_read_root_deve_retornar_ok_ola_mundo(client):
    # Fases do test
    response = client.get('/')  # Act (Ação)
    # Afirmação (garantir)
    assert response.json() == {'message': 'Olá mundo'}
