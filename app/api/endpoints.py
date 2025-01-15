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
from app.core.schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter(tags=["Applications"])

@router.post("/applications", response_model=ApplicationResponse)
async def create_new_application(
    application: ApplicationCreate, db: AsyncSession = Depends(get_db)
) -> ApplicationResponse:
    """
    Эндпоинт для создания новой заявки.
    """
    new_application = await create_application(
        db, user_name=application.user_name, description=application.description
    )
    if not new_application:
        raise HTTPException(status_code=500, detail="Ошибка создания заявки.")
    return new_application  # Здесь возвращаем правильный объект


@router.get("/applications", response_model=List[ApplicationResponse])
async def get_all_applications(
    user_name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
) -> List[ApplicationResponse]:
    """
    Эндпоинт для получения списка заявок с фильтрацией и пагинацией.
    """
    applications = await get_applications(db, user_name=user_name, page=page, size=size)
    return applications  # Убедитесь, что возвращаем список объектов

@router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int, db: AsyncSession = Depends(get_db)
) -> ApplicationResponse:
    """
    Эндпоинт для получения заявки по ID.
    """
    application = await get_application_by_id(db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Заявка не найдена.")
    return application


@router.put("/applications/{application_id}", response_model=ApplicationResponse)
async def update_existing_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """
    Эндпоинт для обновления существующей заявки.
    """
    application = await update_application(
        db, application_id=application_id, **application_update.dict(exclude_unset=True)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Заявка не найдена.")
    return application


@router.delete("/applications/{application_id}", response_model=dict)
async def delete_existing_application(
    application_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Эндпоинт для удаления заявки по ID.
    """
    is_deleted = await delete_application(db, application_id=application_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Заявка не найдена.")
    return {"detail": "Заявка успешно удалена."}
