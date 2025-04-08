import asyncio

from app.database import SessionLocal, async_engine
from app.models import Base, Department, EmployeeManagers, EmployeeStructure, TeamStructure

fixtures = {
    "team_structure": [
        {"team_id": 100, "structure_type": "linear"},
        {"team_id": 200, "structure_type": "functional"},
        {"team_id": 300, "structure_type": "matrix"},
    ],
    "departments": [
        {"team_id": 100, "name": "Разработка", "parent_department_id": None},
        {"team_id": 200, "name": "Разработка", "parent_department_id": None},
        {"team_id": 200, "name": "Тестирование", "parent_department_id": None},
        {"team_id": 300, "name": "Разработка", "parent_department_id": None},
    ],
    "employee_structure": [
        {"user_id": 2, "department_id": 1, "role": "manager", "manager_id": None},
        {"user_id": 1, "department_id": 1, "role": "developer", "manager_id": 2},
        {"user_id": 2, "department_id": 2, "role": "manager", "manager_id": None},
        {"user_id": 1, "department_id": 2, "role": "developer", "manager_id": 2},
        {"user_id": 3, "department_id": 3, "role": "tester", "manager_id": None},
        {"user_id": 2, "department_id": 4, "role": "manager", "manager_id": None},
        {"user_id": 1, "department_id": 4, "role": "developer", "manager_id": 2},
    ],
    "employee_managers": [
        {"employee_structure_id": 7, "manager_id": 3, "context": "project"},
    ],
}


async def load_fixtures():
    """Асинхронная функция для загрузки данных"""
    async with async_engine.begin() as conn:
        # Создаём таблицы
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        # Загружаем TeamStructure
        for ts_data in fixtures["team_structure"]:
            ts = TeamStructure(**ts_data)
            session.add(ts)
        await session.commit()

        # Загружаем Departments
        for dept_data in fixtures["departments"]:
            dept = Department(**dept_data)
            session.add(dept)
        await session.commit()

        # Загружаем EmployeeStructure
        for emp_data in fixtures["employee_structure"]:
            emp = EmployeeStructure(**emp_data)
            session.add(emp)
        await session.commit()

        # Загружаем EmployeeManagers
        for mgr_data in fixtures["employee_managers"]:
            mgr = EmployeeManagers(**mgr_data)
            session.add(mgr)
        await session.commit()

        print("Fixtures loaded successfully!")


# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(load_fixtures())
