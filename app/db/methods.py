from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from .models import Application


async def create_application(session: AsyncSession, user_name: str, description: str) -> Optional[Application]:
    """
    Создает новую заявку в базе данных.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user_name: Имя пользователя.
    :param description: Описание заявки.
    :return: Созданная заявка или None в случае ошибки.
    """
    try:
        new_application = Application(user_name=user_name, description=description)
        session.add(new_application)
        await session.commit()
        await session.refresh(new_application)
        return new_application
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка создания заявки: {e}")
        return None


async def get_applications(
    session: AsyncSession,
    user_name: Optional[str] = None,
    page: int = 1,
    size: int = 10
) -> List[Application]:
    """
    Получает список заявок с фильтрацией и пагинацией.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user_name: Имя пользователя для фильтрации.
    :param page: Номер страницы.
    :param size: Количество записей на странице.
    :return: Список заявок.
    """
    query = select(Application)
    if user_name:
        query = query.where(Application.user_name == user_name)
    query = query.offset((page - 1) * size).limit(size)
    result = await session.execute(query)
    return result.scalars().all()


async def get_application_by_id(session: AsyncSession, application_id: int) -> Optional[Application]:
    """
    Получает заявку по ID.

    :param session: Асинхронная сессия SQLAlchemy.
    :param application_id: Идентификатор заявки.
    :return: Найденная заявка или None, если не найдена.
    """
    query = select(Application).where(Application.id == application_id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_application(
    session: AsyncSession,
    application_id: int,
    user_name: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Application]:
    """
    Обновляет существующую заявку.

    :param session: Асинхронная сессия SQLAlchemy.
    :param application_id: Идентификатор заявки.
    :param user_name: Новое имя пользователя.
    :param description: Новое описание заявки.
    :return: Обновленная заявка или None, если заявка не найдена.
    """
    try:
        query = select(Application).where(Application.id == application_id)
        result = await session.execute(query)
        application = result.scalars().first()

        if not application:
            return None

        if user_name:
            application.user_name = user_name
        if description:
            application.description = description

        await session.commit()
        await session.refresh(application)
        return application
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка обновления заявки: {e}")
        return None


async def delete_application(session: AsyncSession, application_id: int) -> bool:
    """
    Удаляет заявку по ID.

    :param session: Асинхронная сессия SQLAlchemy.
    :param application_id: Идентификатор заявки.
    :return: True, если заявка успешно удалена, иначе False.
    """
    try:
        query = select(Application).where(Application.id == application_id)
        result = await session.execute(query)
        application = result.scalars().first()

        if not application:
            return False

        await session.delete(application)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка удаления заявки: {e}")
        return False
