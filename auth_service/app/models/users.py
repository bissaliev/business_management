import enum
from datetime import datetime

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Status(str, enum.Enum):
    USER = "пользователь"
    ADMIN = "админ"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default=Status.USER)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    deleted_at: Mapped[datetime | None] = None
