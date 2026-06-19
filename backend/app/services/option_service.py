from app.db.connection import get_connection

async def create_option(
    texto: str,
    enquete_id: int
):
    conn = await get_connection()
    try:
        option = await conn.fetchrow(
            """
            INSERT INTO opcoes
            (
                texto,
                enquete_id
            )
            VALUES
            (
                $1,
                $2
            )
            RETURNING *
            """,
            texto,
            enquete_id
        )
        return dict(option)
    finally:
        await conn.close()

async def get_options():
    conn = await get_connection()
    try:
        options = await conn.fetch(
            """
            SELECT *
            FROM opcoes
            ORDER BY id
            """
        )
        return [dict(option) for option in options]
    finally:
        await conn.close()

async def get_option_by_id(option_id: int):
    conn = await get_connection()
    try:
        option = await conn.fetchrow(
            """
            SELECT *
            FROM opcoes
            WHERE id = $1
            """,
            option_id
        )
        return dict(option) if option else None
    finally:
        await conn.close()

async def get_options_by_poll(poll_id: int):
    conn = await get_connection()
    try:
        options = await conn.fetch(
            """
            SELECT *
            FROM opcoes
            WHERE enquete_id = $1
            ORDER BY id
            """,
            poll_id
        )
        return [dict(option) for option in options]
    finally:
        await conn.close()

async def update_option(
    option_id: int,
    texto: str
):
    conn = await get_connection()
    try:
        option = await conn.fetchrow(
            """
            UPDATE opcoes
            SET texto = $1
            WHERE id = $2
            RETURNING *
            """,
            texto,
            option_id
        )
        return dict(option) if option else None
    finally:
        await conn.close()

async def delete_option(option_id: int):
    conn = await get_connection()
    try:
        result = await conn.execute(
            """
            DELETE FROM opcoes
            WHERE id = $1
            """,
            option_id
        )
        return result
    finally:
        await conn.close()