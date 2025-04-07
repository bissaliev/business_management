from sqlalchemy.ext.asyncio import create_async_engine

from app.configs import settings

auth_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.AUTH_USER_DB}:{settings.AUTH_PASSWORD_DB}@{settings.AUTH_DB_HOST}/{settings.AUTH_DB}"
)
