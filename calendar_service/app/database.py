from collections.abc import AsyncIterator, Awaitable
from functools import wraps
from typing import Any, Callable

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


def context_session(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with SessionLocal() as session:
            try:
                result = await func(*args, session=session, **kwargs)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Ошибка в сеансе БД: {str(e)}", exc_info=True)
                raise

    return wrapper
