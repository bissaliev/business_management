from typing import TypeVar

from sqlalchemy import delete, exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    """Базовый репозиторий"""

    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, reference: int) -> ModelType:
        stmt = select(self.model).where(self.model.id == reference)
        result = await self.session.scalars(stmt)
        return result.first()

    async def create(self, **data: dict) -> ModelType:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        stmt = select(self.model)
        result = await self.session.scalars(stmt)
        return result.all()

    async def update(self, reference: int, **update_data: dict):
        stmt = update(self.model).where(self.model.id == reference).values(**update_data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, reference: int) -> None:
        stmt = delete(self.model).where(self.model.id == reference)
        await self.session.execute(stmt)

    async def exists(self, reference: int) -> bool:
        stmt = select(exists(self.model).where(self.model.id == reference))
        result = await self.session.scalar(stmt)
        return result
