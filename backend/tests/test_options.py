from tests.auxiliares import client, create_option, create_poll, unique_value

# Teste para criar uma opção
def test_create_option():
    poll = create_poll()
    response = client.post(
        "/options",
        json={
            "texto": "Python",
            "enquete_id": poll["id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["texto"] == "Python"
    assert response.json()["enquete_id"] == poll["id"]

# Teste para obter uma opção por ID
def test_get_option_by_id():
    data = create_option()
    option = data["option"]
    response = client.get(
        f"/options/{option['id']}"
    )
    assert response.status_code == 200
    assert response.json()["id"] == option["id"]
    assert response.json()["texto"] == option["texto"]
    assert response.json()["enquete_id"] == option["enquete_id"]

# Teste para obter opções de uma enquete
def test_get_options_by_poll():
    data = create_option()
    poll = data["poll"]
    response = client.get(
        f"/options/poll/{poll['id']}"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0

# Teste para atualizar uma opção
def test_update_option():
    data = create_option()
    option = data["option"]
    rand = unique_value()
    response = client.put(
        f"/options/{option['id']}",
        json={
            "texto": f"Updated_{rand}"
        }
    )
    assert response.status_code == 200
    assert response.json()["texto"] == f"Updated_{rand}"

# Teste para deletar uma opção
def test_delete_option():
    data = create_option()
    option = data["option"]
    response = client.delete(
        f"/options/{option['id']}"
    )
    assert response.status_code == 200
    response = client.get(
        f"/options/{option['id']}"
    )
    assert response.status_code == 404 # Verifica se a opção foi realmente deletada