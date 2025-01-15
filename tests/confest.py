from starlette.testclient import TestClient

import pytest_asyncio
import asyncpg
from app.main import app
from httpx import AsyncClient, ASGITransport

# URL базы данных
DATABASE_URL = "postgresql+asyncpg://user:password@db/applications"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_database():
    """
    Очищает базу данных перед каждым тестом, чтобы избежать конфликтов.
    """
    conn = await asyncpg.connect(dsn=DATABASE_URL) #.replace("+asyncpg", ""))
    try:
        # Получаем список всех таблиц
        tables = await conn.fetch(
            """
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            """
        )
        # Удаляем данные из всех таблиц, но не схемы
        for table in tables:
            await conn.execute(f"TRUNCATE TABLE {table['tablename']} RESTART IDENTITY CASCADE")
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="function")
async def test_client():
    """
    Создает асинхронный клиент для тестирования.
    """
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client
