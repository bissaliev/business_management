from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings
from app.logging_config import logger

DATABASE_URL = settings.get_db_postgres_url()


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(url=DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка в сеансе БД: {str(e)}", exc_info=True)
            await session.rollback()
            raise
