from tests.auxiliares import (
    client,
    create_user,
    unique_value
)

# Teste para criação de usuário
def test_create_user():
    rand = unique_value()
    response = client.post(
        "/users",
        json={
            "nome": "Guilherme",
            "email": f"{rand}@email.com",
            "senha": "123456"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert body["nome"] == "Guilherme"
    assert body["email"] == f"{rand}@email.com"

# Teste para obter de usuários
def test_get_users():
    user = create_user()
    response = client.get("/users")
    assert response.status_code == 200
    assert any(
        u["id"] == user["id"]
        for u in response.json()
    )

# Teste para obtenção de usuário por ID
def test_get_user_by_id():
    user = create_user()
    response = client.get(
        f"/users/{user['id']}"
    )
    assert response.status_code == 200
    assert response.json()["id"] == user["id"]

# Teste para atualização de usuário
def test_update_user():
    user = create_user()
    rand = unique_value()
    response = client.put(
        f"/users/{user['id']}",
        json={
            "nome": "Novo Nome",
            "email": f"novo_{rand}@email.com",
            "senha": "abcdef"
        }
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Novo Nome"
    assert response.json()["email"] == f"novo_{rand}@email.com"

# Teste para deletar de usuário
def test_delete_user():
    user = create_user()
    response = client.delete(
        f"/users/{user['id']}"
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user['id']}"
    )
    assert response.status_code == 404 # Verifica se o usuário foi realmente deletado