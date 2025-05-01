import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import TEXT, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    team_code: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4)
    employees: Mapped[list["TeamEmployee"]] = relationship(
        "TeamEmployee", cascade="all, delete-orphan", back_populates="team"
    )
    news: Mapped[list["TeamNews"]] = relationship("TeamNews", cascade="all, delete-orphan", back_populates="team")

    def __str__(self):
        return f"Team: {self.name}"


class TeamEmployee(Base):
    __tablename__ = "team_employee"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    employee_id: Mapped[int]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    role: Mapped[EmployeeRole] = mapped_column(Enum(EmployeeRole, native_enum=False), default=EmployeeRole.EMPLOYEE)

    team: Mapped[Team] = relationship("Team", back_populates="employees")

    __table_args__ = (UniqueConstraint("employee_id", "team_id", name="uq_employee_team"),)

    def __str__(self):
        return f"Employee {self.employee_id} | role {self.role.value}"


class TeamNews(Base):
    __tablename__ = "team_news"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(250))
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    team: Mapped[Team] = relationship("Team", back_populates="news")

    def __str__(self):
        return f"News: {self.title}"
