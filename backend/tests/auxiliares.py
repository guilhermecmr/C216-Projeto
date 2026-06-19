from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Gera um valor único baseado no timestamp atual para evitar conflitos em testes
def unique_value():
    return str(int(datetime.now().timestamp() * 1000000))

# Cria um usuário e retorna os dados do usuário criado
def create_user():
    rand = unique_value()
    response = client.post(
        "/users",
        json={
            "nome": f"User_{rand}",
            "email": f"user_{rand}@email.com",
            "senha": rand
        }
    )
    assert response.status_code == 200
    user = response.json()
    user["senha"] = rand
    return user

# Cria uma enquete e retorna os dados da enquete criada
def create_poll():
    user = create_user()
    response = client.post(
        "/polls",
        json={
            "titulo": f"Poll_{unique_value()}",
            "descricao": "Descrição teste",
            "usuario_id": user["id"]
        }
    )
    assert response.status_code == 200
    return response.json()

# Cria uma opção para uma enquete e retorna os dados da opção criada
def create_option():
    poll = create_poll()
    response = client.post(
        "/options",
        json={
            "texto": f"Option_{unique_value()}",
            "enquete_id": poll["id"]
        }
    )
    assert response.status_code == 200
    return {
        "poll": poll,
        "option": response.json()
    }