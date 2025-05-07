import asyncio
import json

from app.database import SessionLocal, async_engine
from app.models import Base, Department, Division, EmployeeManagers, EmployeeStructure, TeamStructure


def json_to_dict(filename):
    with open(filename, encoding="utf-8") as file:
        content = json.load(file)
        return content


async def load_fixtures(data: dict):
    """Асинхронная функция для загрузки данных"""
    async with async_engine.begin() as conn:
        # Создаём таблицы
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        # Загружаем TeamStructure
        for ts_data in data["team_structure"]:
            ts = TeamStructure(**ts_data)
            session.add(ts)
        await session.commit()

        # Divisions
        for div_data in data["divisions"]:
            session.add(Division(**div_data))
        await session.commit()

        # Загружаем Departments
        for dept_data in data["departments"]:
            dept = Department(**dept_data)
            session.add(dept)
        await session.commit()

        # Загружаем EmployeeStructure
        for emp_data in data["employee_structure"]:
            emp = EmployeeStructure(**emp_data)
            session.add(emp)
        await session.commit()

        # Загружаем EmployeeManagers
        for mgr_data in data["employee_managers"]:
            mgr = EmployeeManagers(**mgr_data)
            session.add(mgr)
        await session.commit()

        print("Fixtures loaded successfully!")


if __name__ == "__main__":
    from pathlib import Path

    current_dir = Path(__file__).parent
    filepath = current_dir / "fixtures.json"
    print(filepath)
    data = json_to_dict(filepath)
    asyncio.run(load_fixtures(data))
