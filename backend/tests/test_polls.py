from tests.auxiliares import client, create_poll, create_user

# Testes para as rotas de enquetes
def test_create_poll():
    user = create_user()
    response = client.post(
        "/polls",
        json={
            "titulo": "Minha enquete",
            "descricao": "Teste",
            "usuario_id": user["id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Minha enquete"

# Teste para obter todas as enquetes
def test_get_polls():
    poll = create_poll()
    response = client.get("/polls")
    assert response.status_code == 200
    assert any(
        p["id"] == poll["id"]
        for p in response.json()
    )

# Teste para obter uma enquete por ID
def test_get_poll_by_id():
    poll = create_poll()
    response = client.get(
        f"/polls/{poll['id']}"
    )
    assert response.status_code == 200
    assert response.json()["id"] == poll["id"]

# Teste para atualizar uma enquete
def test_update_poll():
    poll = create_poll()
    response = client.put(
        f"/polls/{poll['id']}",
        json={
            "titulo": "Atualizada",
            "descricao": "Nova descrição"
        }
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Atualizada"

# Teste para deletar uma enquete
def test_delete_poll():
    poll = create_poll()
    response = client.delete(
        f"/polls/{poll['id']}"
    )
    assert response.status_code == 200
    response = client.get(
        f"/polls/{poll['id']}"
    )   
    assert response.status_code == 404 # Verifica se a enquete foi realmente deletada