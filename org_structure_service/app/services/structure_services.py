from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Department, Division, EmployeeManagers, EmployeeStructure, TeamStructure


class OrgStructureService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team_structure(self, team_id: int) -> dict:
        result = await self.session.execute(select(TeamStructure).where(TeamStructure.team_id == team_id))
        structure = result.scalar_one_or_none()
        structure_type = structure.structure_type if structure else "linear"

        result = await self.session.execute(Division.__table__.select().where(Division.team_id == team_id))
        divisions = [{"id": row.id, "name": row.name} for row in result]

        result = await self.session.execute(Department.__table__.select().where(Department.team_id == team_id))
        departments = [
            {"id": row.id, "name": row.name, "parent_id": row.parent_department_id, "division_id": row.division_id}
            for row in result
        ]

        result = await self.session.execute(
            EmployeeStructure.__table__.select().where(
                EmployeeStructure.department_id.in_([d["id"] for d in departments])
            )
        )
        employees = [
            {
                "id": row.id,
                "employee_id": row.employee_id,
                "dept_id": row.department_id,
                "role": row.role,
                "manager_id": row.manager_id,
            }
            for row in result
        ]

        result = await self.session.execute(
            EmployeeManagers.__table__.select().where(
                EmployeeManagers.employee_structure_id.in_([e["id"] for e in employees])
            )
        )
        extra_managers = [
            {"emp_id": row.employee_structure_id, "manager_id": row.manager_id, "context": row.context}
            for row in result
        ]

        hierarchy = self.build_hierarchy(departments, divisions, employees, extra_managers, structure_type)
        return {"structure_type": structure_type, "hierarchy": hierarchy}

    def build_hierarchy(
        self,
        departments: list[dict],
        divisions: list[dict],
        employees: list[dict],
        extra_managers: list[dict],
        structure_type: str,
    ) -> dict:
        """Вспомогательная функция для построения иерархии"""
        div_map = {div["id"]: {"name": div["name"], "departments": []} for div in divisions}
        dept_map = {
            dept["id"]: {"name": dept["name"], "division_id": dept["division_id"], "children": [], "employees": []}
            for dept in departments
        }
        emp_map = {
            emp["id"]: {
                "employee_id": emp["employee_id"],
                "role": emp["role"],
                "managers": [emp["manager_id"]] if emp["manager_id"] else [],
            }
            for emp in employees
        }

        for mgr in extra_managers:
            if mgr["emp_id"] in emp_map:
                emp_map[mgr["emp_id"]]["managers"].append({"manager_id": mgr["manager_id"], "context": mgr["context"]})

        for emp in employees:
            dept_id = emp["dept_id"]
            if dept_id in dept_map:
                dept_map[dept_id]["employees"].append(emp_map[emp["id"]])

        root_depts = []
        for dept in departments:
            parent_id = dept["parent_id"]
            if structure_type == "divisional" and dept["division_id"]:
                div_map[dept["division_id"]]["departments"].append(dept_map[dept["id"]])
            elif parent_id is None:
                root_depts.append(dept_map[dept["id"]])
            else:
                if parent_id in dept_map:
                    dept_map[parent_id]["children"].append(dept_map[dept["id"]])

        if structure_type == "divisional":
            return {"divisions": list(div_map.values()), "employees": emp_map}
        return {"departments": root_depts if structure_type != "matrix" else dept_map, "employees": emp_map}
