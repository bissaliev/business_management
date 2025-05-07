from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.authentication import authentication_backend
from app.admin.views import UserAdmin
from app.database import async_engine
from app.routers.auth import router as auth_router
from app.routers.users import router as user_router

app = FastAPI(root_path="/users")

admin = Admin(app, async_engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Укажите ваши домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
