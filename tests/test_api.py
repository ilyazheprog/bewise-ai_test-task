from fastapi.testclient import TestClient
import pytest
from app.main import app
from .confest import test_client


@pytest.mark.asyncio
async def test_get_application_by_id(test_client):
    """
    Тест для проверки получения заявки по ID через GET /applications/{application_id}.
    """
    # Создаем заявку для теста
    response = await test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Получаем заявку по ID
    response = await test_client.get(f"/applications/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["user_name"] == "John"
    assert data["description"] == "Test application"


@pytest.mark.asyncio
async def test_update_application(test_client):
    """
    Тест для проверки обновления заявки через PUT /applications/{application_id}.
    """
    # Создаем заявку для теста
    response = await test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Обновляем заявку
    updated_data = {
        "user_name": "John Updated",
        "description": "Updated description"
    }
    response = await test_client.put(f"/applications/{created_id}", json=updated_data)
    assert response.status_code == 200  # Убедимся, что запрос прошёл успешно
    data = response.json()
    assert data["id"] == created_id
    assert data["user_name"] == "John Updated"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_application(test_client):
    """
    Тест для проверки удаления заявки через DELETE /applications/{application_id}.
    """
    # Создаем заявку для теста
    response = await test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Удаляем заявку
    response = await test_client.delete(f"/applications/{created_id}")
    assert response.status_code == 200  # Убедимся, что запрос прошёл успешно
    data = response.json()
    assert data["detail"] == "Заявка успешно удалена"

    # Проверяем, что заявка удалена
    response = await test_client.get(f"/applications/{created_id}")
    assert response.status_code == 404