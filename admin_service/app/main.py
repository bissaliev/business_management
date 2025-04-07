from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker

from app.admin.views import UserModelView
from app.database.auth_database import auth_engine
from app.models.auth import User

app = FastAPI()


Session = sessionmaker(class_=AsyncSession)
Session.configure(binds={User: auth_engine})
admin = Admin(app=app, session_maker=Session)
admin.add_view(UserModelView)
