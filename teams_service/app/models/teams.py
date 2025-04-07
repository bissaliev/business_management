import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import TEXT, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserRole(str, Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    team_code: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4)


class UserTeam(Base):
    __tablename__ = "user_teams"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    role: Mapped[UserRole] = mapped_column(default=UserRole.EMPLOYEE)


class TeamNews(Base):
    __tablename__ = "team_news"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    title: Mapped[str] = mapped_column(String(250))
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


# class Department(Base):
#     __tablename__ = "departments"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(100))
#     team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
#     head_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True)

# team: Mapped[Team] = relationship("Team", back_populates="departments")
# head = relationship("Employee", back_populates="headed_department", foreign_keys=[head_id])
