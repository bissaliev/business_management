from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.dependencies import AuthServiceDeps, CurrentUserDeps
from app.schemas.users import Token, UserCreate, UserResponse

router = APIRouter()


@router.post("/register", summary="Регистрация пользователя")
async def register_user(user_data: UserCreate, user_service: AuthServiceDeps) -> UserResponse:
    return await user_service.create(user_data.model_dump())


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDeps
) -> Token:
    token = await auth_service.login(form_data.username, form_data.password)
    return token


@router.get("/me/")
async def read_users_me(current_user: CurrentUserDeps) -> UserResponse:
    return current_user
