from fastapi import APIRouter

from app.routers.dependencies import UserServiceDeps
from app.schemas.users import UserCreate, UserUpdate

router = APIRouter()


@router.post("/register")
async def register_user(user_service: UserServiceDeps, user_data: UserCreate) -> dict[str, str]:
    user = await user_service.create(user_data.model_dump())
    if user:
        return {"message": "User created"}


@router.put("/{id}")
async def update_user(id: int, user_service: UserServiceDeps, user_data: UserUpdate):
    await user_service.update(id, user_data.model_dump(exclude_unset=True))
    return {"message": "User updated"}


@router.delete("/{id}")
async def delete_user(id: int, user_service: UserServiceDeps):
    await user_service.soft_delete_user(id)
    return {"message": "User deleted"}


@router.post("/restore/{id}")
async def restore_user(id: int, user_service: UserServiceDeps):
    await user_service.restore_user(id)
    return {"message": "User restored"}
