from fastapi.testclient import TestClient
import pytest
from app.main import app
from .confest import test_client


def test_create_application(test_client):
    """
    Тест для проверки создания новой заявки через POST /applications.
    """
    response = test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )
    assert response.status_code == 200  # Убедимся, что запрос прошёл успешно
    data = response.json()
    assert data["user_name"] == "John"
    assert data["description"] == "Test application"
    assert "id" in data  # Убедимся, что возвращается ID
    assert "created_at" in data  # Убедимся, что возвращается дата создания


def test_get_all_applications(test_client):
    """
    Тест для проверки получения всех заявок через GET /applications.
    """
    # Создаем тестовую заявку
    test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )

    response = test_client.get("/applications")
    assert response.status_code == 200  # Убедимся, что запрос прошёл успешно
    data = response.json()
    assert isinstance(data, list)  # Убедимся, что возвращается список
    if data:
        assert "user_name" in data[0]
        assert "description" in data[0]
        assert "id" in data[0]
        assert "created_at" in data[0]


def test_get_application_by_id(test_client):
    """
    Тест для проверки получения заявки по ID через GET /applications/{application_id}.
    """
    # Создаем заявку для теста
    response = test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Получаем заявку по ID
    response = test_client.get(f"/applications/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["user_name"] == "John"
    assert data["description"] == "Test application"


def test_update_application(test_client):
    """
    Тест для проверки обновления заявки через PUT /applications/{application_id}.
    """
    # Создаем заявку для теста
    response = test_client.post(
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
    response = test_client.put(f"/applications/{created_id}", json=updated_data)
    assert response.status_code == 200  # Убедимся, что запрос прошёл успешно
    data = response.json()
    assert data["id"] == created_id
    assert data["user_name"] == "John Updated"
    assert data["description"] == "Updated description"


def test_delete_application(test_client):
    """
    Тест для проверки удаления заявки через DELETE /applications/{application_id}.
    """
    # Создаем заявку для теста
    response = test_client.post(
        "/applications",
        json={
            "user_name": "John",
            "description": "Test application"
        },
    )
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Удаляем заявку
    response = test_client.delete(f"/applications/{created_id}")
    assert response.status_code == 200  # Убедимся, что запрос прошёл успешно
    data = response.json()
    assert data["detail"] == "Заявка успешно удалена"

    # Проверяем, что заявка удалена
    response = test_client.get(f"/applications/{created_id}")
    assert response.status_code == 404
