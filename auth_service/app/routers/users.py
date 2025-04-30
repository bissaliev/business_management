from fastapi import APIRouter, status

from app.routers.dependencies import CurrentUserDeps, RequiredAdminDeps, UserServiceDeps
from app.schemas.users import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserResponse, summary="Регистрация пользователя")
async def register_user(user_data: UserCreate, user_service: UserServiceDeps) -> UserResponse:
    return await user_service.create(user_data.model_dump())


@router.get("/", response_model=list[UserResponse], summary="Получение пользователей")
async def get_users(user_service: UserServiceDeps) -> list[UserResponse]:
    return await user_service.get_users()


@router.get("/{id}", response_model=UserResponse, summary="Получение пользователя")
async def get_user(id: int, user_service: UserServiceDeps) -> UserResponse:
    return await user_service.get_user(id)


@router.put(
    "/{id}", response_model=UserResponse, dependencies=[RequiredAdminDeps], summary="Обновление данных пользователя"
)
async def update_user(id: int, user_data: UserUpdate, user_service: UserServiceDeps) -> UserResponse:
    return await user_service.update(id, user_data.model_dump(exclude_unset=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[RequiredAdminDeps],
    summary="Удаление пользователя с возможность восстановления",
)
async def soft_delete_user(id: int, user_service: UserServiceDeps) -> None:
    await user_service.soft_delete_user(id)


@router.patch(
    "/{id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[RequiredAdminDeps],
    summary="Восстановление пользователя",
)
async def restore_user(id: int, user_service: UserServiceDeps) -> None:
    await user_service.restore_user(id)


@router.get("/me/", response_model=UserResponse, summary="Получение профиля пользователя")
async def read_users_me(current_user: CurrentUserDeps, user_service: UserServiceDeps) -> UserResponse:
    return await user_service.get_user(current_user.id)


@router.put("/me/", response_model=UserResponse, summary="Обновление профиля пользователя")
async def update_users_me(
    current_user: CurrentUserDeps, user_data: UserUpdate, user_service: UserServiceDeps
) -> UserResponse:
    return await user_service.update(current_user.id, user_data.model_dump(exclude_unset=True))
