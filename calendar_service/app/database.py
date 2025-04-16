from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DATABASE_URL = settings.get_db_postgres_url()


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(url=DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session
        await session.commit()
