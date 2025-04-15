from typing import TypeVar

from sqlalchemy import exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, **data: dict) -> ModelType:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, reference: int) -> ModelType:
        stmt = select(self.model).where(self.model.id == reference)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        result = await self.session.scalars(select(self.model))
        return result.all()

    async def update(self, reverence: int, **data: dict) -> ModelType:
        stmt = update(self.model).where(self.model.id == reverence).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, reference: int) -> bool:
        stmt = select(exists(self.model).where(self.model.id == reference))
        result = await self.session.execute(stmt)
        return result.scalar()
