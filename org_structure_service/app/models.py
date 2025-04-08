from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StructureType(str, Enum):
    LINEAR = "Линейная"
    FUNCTIONAL = "Функциональная"
    MATRIX = "Матричная"


class TeamStructure(Base):
    """Структура команды"""

    __tablename__ = "team_structure"

    team_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    structure_type: Mapped[StructureType] = mapped_column(String, default=StructureType.LINEAR)

    departments: Mapped[list["Department"]] = relationship("Department", back_populates="team_structure")


class Department(Base):
    """Отдел"""

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team_structure.team_id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)

    team_structure: Mapped["TeamStructure"] = relationship("TeamStructure", back_populates="departments")
    parent_department: Mapped[Optional["Department"]] = relationship(
        "Department", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Department"]] = relationship("Department", back_populates="parent_department")
    employees: Mapped[list["EmployeeStructure"]] = relationship("EmployeeStructure", back_populates="department")


class EmployeeStructure(Base):
    """Структура сотрудников"""

    __tablename__ = "employee_structure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Ссылка на User Service
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    manager_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Основной руководитель

    department: Mapped[Optional["Department"]] = relationship("Department", back_populates="employees")
    extra_managers: Mapped[list["EmployeeManagers"]] = relationship("EmployeeManagers", back_populates="employee")


class EmployeeManagers(Base):
    """Дополнительные руководители (для матричной структуры)"""

    __tablename__ = "employee_managers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_structure_id: Mapped[int] = mapped_column(ForeignKey("employee_structure.id"), nullable=False)
    manager_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Ссылка на User Service
    context: Mapped[str] = mapped_column(String, nullable=False)  # "project", "function" и т.д.

    employee: Mapped["EmployeeStructure"] = relationship("EmployeeStructure", back_populates="extra_managers")
