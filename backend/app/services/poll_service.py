from app.db.connection import get_connection

async def create_poll(
    titulo: str,
    descricao: str,
    usuario_id: int
):
    conn = await get_connection()
    try:
        poll = await conn.fetchrow(
            """
            INSERT INTO enquetes
            (
                titulo,
                descricao,
                usuario_id
            )
            VALUES
            (
                $1,
                $2,
                $3
            )
            RETURNING *
            """,
            titulo,
            descricao,
            usuario_id
        )
        return dict(poll)
    finally:
        await conn.close()

async def get_polls():
    conn = await get_connection()
    try:
        polls = await conn.fetch(
            """
            SELECT *
            FROM enquetes
            ORDER BY created_at DESC
            """
        )
        return [dict(poll) for poll in polls]
    finally:
        await conn.close()

async def get_poll_by_id(poll_id: int):
    conn = await get_connection()
    try:
        poll = await conn.fetchrow(
            """
            SELECT *
            FROM enquetes
            WHERE id = $1
            """,
            poll_id
        )
        return dict(poll) if poll else None
    finally:
        await conn.close()

async def update_poll(
    poll_id: int,
    titulo: str,
    descricao: str
):
    conn = await get_connection()
    try:
        poll = await conn.fetchrow(
            """
            UPDATE enquetes
            SET titulo = $1,
                descricao = $2
            WHERE id = $3
            RETURNING *
            """,
            titulo,
            descricao,
            poll_id
        )
        return dict(poll) if poll else None
    finally:
        await conn.close()

async def delete_poll(poll_id: int):
    conn = await get_connection()
    try:
        result = await conn.execute(
            """
            DELETE FROM enquetes
            WHERE id = $1
            """,
            poll_id
        )
        return result
    finally:
        await conn.close()

async def get_poll_results(poll_id: int):
    conn = await get_connection()
    try:
        poll = await conn.fetchrow(
            """
            SELECT id, titulo
            FROM enquetes
            WHERE id = $1
            """,
            poll_id
        )
        if not poll:
            return None
        total_votes = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM votos
            WHERE enquete_id = $1
            """,
            poll_id
        )
        options = await conn.fetch(
            """
            SELECT
                o.id,
                o.texto,
                COUNT(v.id) AS votos
            FROM opcoes o
            LEFT JOIN votos v
                ON v.opcao_id = o.id
            WHERE o.enquete_id = $1
            GROUP BY o.id, o.texto
            ORDER BY o.id
            """,
            poll_id
        )
        result_options = []
        for option in options:
            vote_count = int(option["votos"])
            percentage = (
                round((vote_count / total_votes) * 100, 2)
                if total_votes > 0
                else 0
            )
            result_options.append({
                "id": option["id"],
                "texto": option["texto"],
                "votos": vote_count,
                "percentual": percentage
            })
        return {
            "poll_id": poll["id"],
            "titulo": poll["titulo"],
            "total_votos": total_votes,
            "opcoes": result_options
        }
    finally:
        await conn.close()