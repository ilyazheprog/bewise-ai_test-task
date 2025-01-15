import pytest
import asyncpg
from app.main import app
from fastapi.testclient import TestClient

# URL базы данных
DATABASE_URL = "postgresql+asyncpg://user:password@db/applications"


@pytest.fixture(scope="function", autouse=True)
async def setup_test_database():
    """
    Очищает базу данных перед каждым тестом, чтобы избежать конфликтов.
    """
    conn = await asyncpg.connect(dsn=DATABASE_URL.replace("+asyncpg", ""))
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


@pytest.fixture(scope="function")
def test_client():
    """
    Создает клиент для тестирования.
    """
    with TestClient(app) as client:
        yield client
