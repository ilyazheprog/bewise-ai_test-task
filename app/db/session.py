from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create an asynchronous engine with connection pooling parameters
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# Create a sessionmaker factory bound to the engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Dependency to provide a database session
async def get_db():
    async with SessionLocal() as session:
        yield session
