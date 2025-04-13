from sqladmin import ModelView

from app.models.users import User
from app.security import get_password_hash


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email, User.status, User.is_active]
    column_labels = {"hashed_password": "Password"}

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            # Hash the password before saving into DB !
            data["hashed_password"] = get_password_hash(data["hashed_password"])
