from jose import JWTError, jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.database import SessionLocal
from app.security import create_access_token, verify_password
from app.services.user_service import UserService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        async with SessionLocal() as session:
            user_service = UserService(session)
            user = await user_service.get_user_by_email(email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        access_token = create_access_token({"sub": str(user.id)})
        request.session.update({"token": str(access_token)})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                return False
        except JWTError:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
