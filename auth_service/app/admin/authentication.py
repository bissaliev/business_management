from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.database import SessionLocal
from app.logging_config import logger
from app.services.auth_service import AuthService


class AdminAuth(AuthenticationBackend):
    """Аутентификация в админ панели"""

    auth_service = AuthService

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        async with SessionLocal() as session:
            service = self.auth_service(session)
            token = await service.login(email, password)
        logger.info(f"Администратор {email} вошел в систему")
        request.session.update({"token": str(token.access_token)})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        async with SessionLocal() as session:
            service = self.auth_service(session)
            user = await service.get_current_admin(token)
            if user is None:
                return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
