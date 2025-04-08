import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import TEXT, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EmployeeRole(str, Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    team_code: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4)


class TeamEmployee(Base):
    __tablename__ = "team_employee"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    employee_id: Mapped[int]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    role: Mapped[EmployeeRole] = mapped_column(default=EmployeeRole.EMPLOYEE)


class TeamNews(Base):
    __tablename__ = "team_news"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    title: Mapped[str] = mapped_column(String(250))
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
