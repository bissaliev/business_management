from fastapi import FastAPI
from sqladmin import Admin

from app.admin.authentication import authentication_backend
from app.admin.views import UserAdmin
from app.database import async_engine
from app.routers.users import router as user_router

app = FastAPI()

admin = Admin(app, async_engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)


app.include_router(user_router, prefix="/users", tags=["users"])
