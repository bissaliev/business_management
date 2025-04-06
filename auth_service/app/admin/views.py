from sqladmin import ModelView

from app.models.users import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email, User.status, User.is_active]
