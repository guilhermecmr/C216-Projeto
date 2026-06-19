import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/votacao_db"
)

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)