import json
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
from app.core.logger import logger
from app.kafka.producer import send_message as send_msg_prod
from app.core.config import settings

app_router = APIRouter(tags=["Applications"])

@app_router.post("/applications", response_model=ApplicationResponse)
async def create_new_application(
    application: ApplicationCreate, db: AsyncSession = Depends(get_db)
) -> ApplicationResponse:
    """
    Эндпоинт для создания новой заявки.
    """
    try:
        new_application = await create_application(
            db, user_name=application.user_name, description=application.description
        )
        if not new_application:
            logger.error("Failed to create application: %s", application.model_dump())
            raise HTTPException(status_code=500, detail="Ошибка создания заявки.")
        
        application_dict = application.model_dump()
        logger.info("Application created successfully: %s", application_dict)

        await send_msg_prod(settings.KAFKA_TOPIC, json.dumps(application_dict))
    
        return new_application
    except Exception as e:
        logger.exception("Unexpected error during application creation: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app_router.get("/applications", response_model=List[ApplicationResponse])
async def get_all_applications(
    user_name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
) -> List[ApplicationResponse]:
    """
    Эндпоинт для получения списка заявок с фильтрацией и пагинацией.
    """
    try:
        applications = await get_applications(db, user_name=user_name, page=page, size=size)
        logger.info("Fetched applications for user '%s': %s items", user_name, len(applications))
        return applications
    except Exception as e:
        logger.exception("Error fetching applications: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app_router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int, db: AsyncSession = Depends(get_db)
) -> ApplicationResponse:
    """
    Эндпоинт для получения заявки по ID.
    """
    try:
        application = await get_application_by_id(db, application_id=application_id)
        if not application:
            logger.warning("Application with ID %d not found", application_id)
            raise HTTPException(status_code=404, detail="Заявка не найдена.")
        logger.info("Fetched application: %s", application)
        return application
    except Exception as e:
        logger.exception("Error fetching application by ID %d: %s", application_id, str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app_router.put("/applications/{application_id}", response_model=ApplicationResponse)
async def update_existing_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """
    Эндпоинт для обновления существующей заявки.
    """
    try:
        application = await update_application(
            db, application_id=application_id, **application_update.dict(exclude_unset=True)
        )
        if not application:
            logger.warning("Failed to update application. ID %d not found.", application_id)
            raise HTTPException(status_code=404, detail="Заявка не найдена.")
        logger.info("Application id=%d updated successfully", application_id)
        return application
    except Exception as e:
        logger.exception("Error updating application ID %d: %s", application_id, str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app_router.delete("/applications/{application_id}", response_model=dict)
async def delete_existing_application(
    application_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Эндпоинт для удаления заявки по ID.
    """
    try:
        is_deleted = await delete_application(db, application_id=application_id)
        if not is_deleted:
            logger.warning("Failed to delete application. ID %d not found.", application_id)
            raise HTTPException(status_code=404, detail="Заявка не найдена.")
        logger.info("Application with ID %d deleted successfully", application_id)
        return {"detail": "Заявка успешно удалена."}
    except Exception as e:
        logger.exception("Error deleting application ID %d: %s", application_id, str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
