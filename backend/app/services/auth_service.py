from app.db.connection import get_connection

async def login(email: str, senha: str):
    conn = await get_connection()
    try:
        user = await conn.fetchrow(
            """
            SELECT id, nome, email
            FROM usuarios
            WHERE email = $1
            AND senha = $2
            """,
            email,
            senha
        )
        return dict(user) if user else None
    finally:
        await conn.close()