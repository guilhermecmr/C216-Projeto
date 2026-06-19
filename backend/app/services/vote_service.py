from app.db.connection import get_connection

async def user_exists(user_id: int):
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT EXISTS(
                SELECT 1
                FROM usuarios
                WHERE id = $1
            )
            """,
            user_id
        )
        return result
    finally:
        await conn.close()

async def poll_exists(poll_id: int):
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT EXISTS(
                SELECT 1
                FROM enquetes
                WHERE id = $1
            )
            """,
            poll_id
        )
        return result
    finally:
        await conn.close()

async def option_exists(option_id: int):
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT EXISTS(
                SELECT 1
                FROM opcoes
                WHERE id = $1
            )
            """,
            option_id
        )
        return result
    finally:
        await conn.close()

async def option_belongs_to_poll(
    option_id: int,
    poll_id: int
):
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT EXISTS(
                SELECT 1
                FROM opcoes
                WHERE id = $1
                AND enquete_id = $2
            )
            """,
            option_id,
            poll_id
        )
        return result
    finally:
        await conn.close()

async def user_already_voted(
    user_id: int,
    poll_id: int
):
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT EXISTS(
                SELECT 1
                FROM votos
                WHERE usuario_id = $1
                AND enquete_id = $2
            )
            """,
            user_id,
            poll_id
        )
        return result
    finally:
        await conn.close()

async def register_vote(
    user_id: int,
    poll_id: int,
    option_id: int
):
    conn = await get_connection()
    try:
        vote = await conn.fetchrow(
            """
            INSERT INTO votos
            (
                usuario_id,
                enquete_id,
                opcao_id
            )
            VALUES
            (
                $1,
                $2,
                $3
            )
            RETURNING *
            """,
            user_id,
            poll_id,
            option_id
        )
        return dict(vote)
    finally:
        await conn.close()