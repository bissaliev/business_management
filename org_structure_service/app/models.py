import enum
from typing import Optional

from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StructureType(str, enum.Enum):
    LINEAR = "Линейная"
    FUNCTIONAL = "Функциональная"
    MATRIX = "Матричная"
    DIVISIONAL = "Дивизиональная"
    LINEAR_FUNCTIONAL = "Линейно-функциональная"


class EmployeeRole(str, enum.Enum):
    EMPLOYEE = "сотрудник"
    MANAGER = "менеджер"
    ADMINISTRATOR = "админ"


class TeamStructure(Base):
    """Структура команды"""

    __tablename__ = "team_structure"

    team_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    structure_type: Mapped[StructureType] = mapped_column(
        Enum(StructureType, native_enum=False), default=StructureType.LINEAR
    )

    divisions: Mapped[list["Division"]] = relationship("Division", back_populates="team_structure")
    departments: Mapped[list["Department"]] = relationship("Department", back_populates="team_structure")

    def __repr__(self):
        return f"{self.__class__.__name__}(team_id={self.team_id}, structure_type={self.structure_type})"


class Division(Base):
    __tablename__ = "divisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team_structure.team_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    team_structure: Mapped["TeamStructure"] = relationship("TeamStructure", back_populates="divisions")
    departments: Mapped[list["Department"]] = relationship("Department", back_populates="division")

    __table_args__ = (UniqueConstraint("team_id", "name", name="uq_division_team_name"),)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, team_id={self.team_id}, name={self.name})"


class Department(Base):
    """Отдел"""

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team_structure.team_id"), nullable=False)
    division_id: Mapped[int | None] = mapped_column(ForeignKey("divisions.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)

    team_structure: Mapped["TeamStructure"] = relationship("TeamStructure", back_populates="departments")
    division: Mapped[Optional["Division"]] = relationship("Division", back_populates="departments")
    parent_department: Mapped[Optional["Department"]] = relationship(
        "Department", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Department"]] = relationship("Department", back_populates="parent_department")
    employees: Mapped[list["EmployeeStructure"]] = relationship("EmployeeStructure", back_populates="department")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, team_id={self.team_id}, name={self.name})"


class EmployeeStructure(Base):
    """Структура сотрудников"""

    __tablename__ = "employee_structure"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int]  # Ссылка на User Service
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    position: Mapped[str] = mapped_column(String(255), nullable=False)  # position
    manager_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Основной руководитель

    department: Mapped[Optional["Department"]] = relationship("Department", back_populates="employees")
    extra_managers: Mapped[list["EmployeeManagers"]] = relationship("EmployeeManagers", back_populates="employee")

    __table_args__ = (UniqueConstraint("employee_id", "department_id", name="uq_employee_department"),)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, employee_id={self.employee_id})"


class EmployeeManagers(Base):
    """Дополнительные руководители (для матричной структуры)"""

    __tablename__ = "employee_managers"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_structure_id: Mapped[int] = mapped_column(ForeignKey("employee_structure.id"), nullable=False)
    manager_id: Mapped[int]  # Ссылка на User Service
    context: Mapped[str]  # "project", "function" и т.д.

    employee: Mapped["EmployeeStructure"] = relationship("EmployeeStructure", back_populates="extra_managers")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, employee_structure_id={self.employee_structure_id}, manager_id={self.manager_id})"
        )
