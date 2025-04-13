from fastapi import APIRouter

from app.routers.dependencies import UserServiceDeps
from app.schemas.users import Message, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", summary="Получение пользователей")
async def get_users(user_service: UserServiceDeps) -> list[UserResponse]:
    return await user_service.get_users()


@router.get("/{id}", summary="Получение пользователя")
async def get_user(id: int, user_service: UserServiceDeps) -> UserResponse:
    return await user_service.get_user(id)


@router.put("/{id}", summary="Обновление данных пользователя")
async def update_user(id: int, user_data: UserUpdate, user_service: UserServiceDeps) -> UserResponse:
    return await user_service.update(id, user_data.model_dump(exclude_unset=True))


@router.delete("/{id}", summary="Удаление пользователя с возможность восстановления")
async def soft_delete_user(id: int, user_service: UserServiceDeps) -> Message:
    await user_service.soft_delete_user(id)
    return Message(message="Пользователь временно удален")


@router.post("/{id}/restore", summary="Восстановление пользователя")
async def restore_user(id: int, user_service: UserServiceDeps) -> Message:
    await user_service.restore_user(id)
    return Message(message="Пользователь восстановлен")
