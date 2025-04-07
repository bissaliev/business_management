from sqladmin import ModelView

from app.models.auth import User


class UserModelView(ModelView, model=User):
    column_list = ["id", "name", "email", "team_id", "status"]
