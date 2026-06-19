from app.db.connection import get_connection

async def create_user(nome: str, email: str, senha: str):
    conn = await get_connection()
    try:
        user = await conn.fetchrow(
            """
            INSERT INTO usuarios (nome, email, senha)
            VALUES ($1, $2, $3)
            RETURNING id, nome, email
            """,
            nome,
            email,
            senha
        )
        return dict(user)
    finally:
        await conn.close()

async def get_users():
    conn = await get_connection()
    try:
        users = await conn.fetch(
            """
            SELECT id, nome, email
            FROM usuarios
            ORDER BY id
            """
        )
        return [dict(user) for user in users]
    finally:
        await conn.close()

async def get_user_by_id(user_id: int):
    conn = await get_connection()
    try:
        user = await conn.fetchrow(
            """
            SELECT id, nome, email
            FROM usuarios
            WHERE id = $1
            """,
            user_id
        )
        return dict(user) if user else None
    finally:
        await conn.close()

async def update_user(
    user_id: int,
    nome: str,
    email: str,
    senha: str
):
    conn = await get_connection()
    try:
        user = await conn.fetchrow(
            """
            UPDATE usuarios
            SET nome = $1,
                email = $2,
                senha = $3
            WHERE id = $4
            RETURNING id, nome, email
            """,
            nome,
            email,
            senha,
            user_id
        )
        return dict(user) if user else None
    finally:
        await conn.close()

async def delete_user(user_id: int):
    conn = await get_connection()
    try:
        result = await conn.execute(
            """
            DELETE FROM usuarios
            WHERE id = $1
            """,
            user_id
        )
        return result
    finally:
        await conn.close()