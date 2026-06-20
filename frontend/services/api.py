import os
import httpx

API_URL = os.getenv(
    "API_URL",
    "http://backend:8000"
)

async def login_user(
    email: str,
    senha: str
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "senha": senha
            }
        )
    return response

async def register_user(
    nome: str,
    email: str,
    senha: str
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/users",
            json={
                "nome": nome,
                "email": email,
                "senha": senha
            }
        )
    return response

async def get_polls():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/polls"
        )
    return response

async def create_poll(
    titulo: str,
    descricao: str,
    usuario_id: int
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/polls",
            json={
                "titulo": titulo,
                "descricao": descricao,
                "usuario_id": usuario_id
            }
        )
    return response

async def get_poll_by_id(
    poll_id: int
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/polls/{poll_id}"
        )
    return response

async def update_poll(
    poll_id: int,
    titulo: str,
    descricao: str
):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_URL}/polls/{poll_id}",
            json={
                "titulo": titulo,
                "descricao": descricao
            }
        )
    return response

async def delete_poll(poll_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{API_URL}/polls/{poll_id}"
        )
    return response

async def get_options_by_poll(
    poll_id: int
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/options/poll/{poll_id}"
        )
    return response

async def create_option(
    texto: str,
    enquete_id: int
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/options",
            json={
                "texto": texto,
                "enquete_id": enquete_id
            }
        )
    return response

async def update_option(
    option_id: int,
    texto: str
):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_URL}/options/{option_id}",
            json={
                "texto": texto
            }
        )
    return response

async def delete_option(option_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{API_URL}/options/{option_id}"
        )
    return response

async def vote(
    usuario_id: int,
    enquete_id: int,
    opcao_id: int
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/votes",
            json={
                "usuario_id": usuario_id,
                "enquete_id": enquete_id,
                "opcao_id": opcao_id
            }
        )
    return response

async def get_poll_results(
    poll_id: int
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/polls/results/{poll_id}"
        )
    return response