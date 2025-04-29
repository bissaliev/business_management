from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.dependencies import AuthServiceDeps, CurrentUserDeps
from app.schemas.users import Token, UserTokenResponse

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDeps
) -> Token:
    token = await auth_service.login(form_data.username, form_data.password)
    return token


@router.get("/verify", response_model=UserTokenResponse, summary="Верификация токена")
async def verify_token(user: CurrentUserDeps) -> UserTokenResponse:
    return user
