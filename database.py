"""
Configuración de la Base de Datos - SQLAlchemy Async
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from models import Base

# Motor de base de datos asíncrono
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Mostrar SQL en desarrollo
    future=True
)

# Sesión asíncrona
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Crear todas las tablas en la base de datos"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency para obtener sesión de BD en endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
