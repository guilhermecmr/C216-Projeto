from tests.auxiliares import client, create_user, unique_value

# Teste de login com sucesso
def test_login_success():
    user = create_user()
    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "senha": user["senha"]
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["nome"] == user["nome"]
    assert response.json()["email"] == user["email"]

# Teste de login com email inexistente
def test_login_invalid_email():
    response = client.post(
        "/auth/login",
        json={
            "email": f"{unique_value()}@email.com",
            "senha": "123456"
        }
    )
    assert response.status_code == 401

# Teste de login com senha incorreta
def test_login_invalid_password():
    user = create_user()
    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "senha": "senha_errada"
        }
    )
    assert response.status_code == 401

# Teste de login com email e senha incorretos
def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={
            "email": f"{unique_value()}@email.com",
            "senha": "senha_errada"
        }
    )
    assert response.status_code == 401

# Teste de login após atualizar usuário
def test_login_after_user_update():
    user = create_user()
    rand = unique_value()
    response = client.put(
        f"/users/{user['id']}",
        json={
            "nome": f"Updated_{rand}",
            "email": f"updated_{rand}@email.com",
            "senha": "nova_senha"
        }
    )
    assert response.status_code == 200
    old_login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "senha": user["senha"]
        }
    )
    assert old_login.status_code == 401
    new_login = client.post(
        "/auth/login",
        json={
            "email": f"updated_{rand}@email.com",
            "senha": "nova_senha"
        }
    )
    assert new_login.status_code == 200

# Teste de login após deletar usuário
def test_login_after_user_delete():
    user = create_user()
    response = client.delete(
        f"/users/{user['id']}"
    )
    assert response.status_code == 200
    login = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "senha": user["senha"]
        }
    )
    assert login.status_code == 401