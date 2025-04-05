from datetime import datetime

import httpx
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_password_hash
from app.config import settings
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, id: int):
    stmt = select(User).where(User.id == id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_user(db: AsyncSession, user_data: UserCreate):
    new_data = user_data.model_dump()
    password = new_data.pop("password")
    hashed_password = pwd_context.hash(password)
    new_data["hashed_password"] = hashed_password
    db_user = User(**new_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, id: int, user_data: UserUpdate):
    update_date = UserUpdate.model_dump(exclude_unset=True)
    stmt = update(User).where(User.id == id).values(**update_date).returning(User)
    result = await db.scalars(stmt)
    await db.commit()
    return result.first()


async def delete_user(db: AsyncSession, id: int):
    stmt = update(User).where(User.id == id).values(is_active=False, deleted_at=datetime.now())
    await db.execute(stmt)
    await db.commit()


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user_by_id(self, id: int):
        result = await self.session.execute(select(User).where(User.id == id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не существует")
        return user

    async def create(self, user_data: dict):
        email = user_data["email"]
        user = await self.get_user_by_email(email)
        if user:
            raise HTTPException(status_code=400, detail="Пользователь с таким email существует")

        team_code = user_data.pop("team_code")
        try:
            async with httpx.AsyncClient() as client:
                url = settings.get_team_by_code_url()
                team_response = await client.get(f"{url}/{team_code}")
                if team_response.status_code == 200:
                    team_id = team_response.json()["id"]
        except httpx.ConnectError:
            team_id = 1

        password = user_data.pop("password")
        hashed_password = get_password_hash(password)
        user_data["hashed_password"] = hashed_password
        user_data["team_id"] = team_id
        db_user = User(**user_data)
        self.session.add(db_user)
        return db_user

    async def update(self, id: int, user_data: dict):
        user_db = await self.get_user_by_id(id)
        await self.session.execute(update(User).where(User.id == user_db.id).values(**user_data))

    async def soft_delete_user(self, id: int):
        user_db = await self.get_user_by_id(id)
        user_db.deleted_at = datetime.now()
        user_db.is_active = False

    async def restore_user(self, id: int):
        user_db = await self.get_user_by_id(id)
        user_db.deleted_at = None
        user_db.is_active = True
