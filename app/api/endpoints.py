from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.db.models import Application
from app.db.methods import (
    create_application,
    get_applications,
    get_application_by_id,
    update_application,
    delete_application,
)

router = APIRouter(tags=["Applications"])


@router.post("/applications", response_model=dict)
async def create_new_application(
    user_name: str, description: str, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Эндпоинт для создания новой заявки.
    """
    application = await create_application(db, user_name=user_name, description=description)
    if not application:
        raise HTTPException(status_code=500, detail="Ошибка создания заявки.")
    return {
        "id": application.id,
        "user_name": application.user_name,
        "description": application.description,
        "created_at": application.created_at,
    }


@router.get("/applications", response_model=List[dict])
async def get_all_applications(
    user_name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """
    Эндпоинт для получения списка заявок с фильтрацией и пагинацией.
    """
    applications = await get_applications(db, user_name=user_name, page=page, size=size)
    return [
        {
            "id": app.id,
            "user_name": app.user_name,
            "description": app.description,
            "created_at": app.created_at,
        }
        for app in applications
    ]


@router.get("/applications/{application_id}", response_model=dict)
async def get_application(application_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Эндпоинт для получения заявки по ID.
    """
    application = await get_application_by_id(db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Заявка не найдена.")
    return {
        "id": application.id,
        "user_name": application.user_name,
        "description": application.description,
        "created_at": application.created_at,
    }


@router.put("/applications/{application_id}", response_model=dict)
async def update_existing_application(
    application_id: int,
    user_name: Optional[str] = None,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Эндпоинт для обновления существующей заявки.
    """
    application = await update_application(
        db, application_id=application_id, user_name=user_name, description=description
    )
    if not application:
        raise HTTPException(status_code=404, detail="Заявка не найдена.")
    return {
        "id": application.id,
        "user_name": application.user_name,
        "description": application.description,
        "created_at": application.created_at,
    }


@router.delete("/applications/{application_id}", response_model=dict)
async def delete_existing_application(application_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Эндпоинт для удаления заявки по ID.
    """
    is_deleted = await delete_application(db, application_id=application_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Заявка не найдена.")
    return {"detail": "Заявка успешно удалена."}
