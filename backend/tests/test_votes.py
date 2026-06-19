from tests.auxiliares import client, create_user, create_poll

# Teste para registro de voto
def test_register_vote():
    user = create_user()
    poll = create_poll()
    option = client.post(
        "/options",
        json={
            "texto": "Python",
            "enquete_id": poll["id"]
        }
    ).json()
    response = client.post(
        "/votes",
        json={
            "usuario_id": user["id"],
            "enquete_id": poll["id"],
            "opcao_id": option["id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["usuario_id"] == user["id"]
    assert response.json()["enquete_id"] == poll["id"]
    assert response.json()["opcao_id"] == option["id"]

# Teste para voto duplicado
def test_duplicate_vote():
    user = create_user()
    poll = create_poll()
    option = client.post(
        "/options",
        json={
            "texto": "Python",
            "enquete_id": poll["id"]
        }
    ).json()
    client.post(
        "/votes",
        json={
            "usuario_id": user["id"],
            "enquete_id": poll["id"],
            "opcao_id": option["id"]
        }
    )
    response = client.post(
        "/votes",
        json={
            "usuario_id": user["id"],
            "enquete_id": poll["id"],
            "opcao_id": option["id"]
        }
    )
    assert response.status_code == 400

# Teste para resultados da enquete
def test_poll_results():
    user = create_user()
    poll = create_poll()
    option = client.post(
        "/options",
        json={
            "texto": "Python",
            "enquete_id": poll["id"]
        }
    ).json()
    client.post(
        "/votes",
        json={
            "usuario_id": user["id"],
            "enquete_id": poll["id"],
            "opcao_id": option["id"]
        }
    )
    response = client.get(
        f"/polls/results/{poll['id']}"
    )
    assert response.status_code == 200
    body = response.json()
    assert body["poll_id"] == poll["id"]
    assert body["total_votos"] == 1