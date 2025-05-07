import asyncio
import json

from app.database import SessionLocal, async_engine
from app.models.teams import Base, Team, TeamEmployee, TeamNews


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
        # Загружаем Team
        for ts_data in data["teams"]:
            ts = Team(**ts_data)
            session.add(ts)
        await session.commit()

        # Загружаем TeamEmployee
        for div_data in data["team_employee"]:
            session.add(TeamEmployee(**div_data))
        await session.commit()

        # Загружаем TeamNews
        for dept_data in data["team_news"]:
            dept = TeamNews(**dept_data)
            session.add(dept)
        await session.commit()

        print("================Фикстуры загружен в БД!===============")


if __name__ == "__main__":
    from pathlib import Path

    current_dir = Path(__file__).parent
    filepath = current_dir / "fixtures.json"
    print(filepath)
    data = json_to_dict(filepath)
    asyncio.run(load_fixtures(data))
