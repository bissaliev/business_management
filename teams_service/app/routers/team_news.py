from fastapi import APIRouter, status

from app.routers.dependencies import AdminDeps, TeamNewsServiceDeps
from app.schemas.team_news import TeamNewsCreate, TeamNewsResponse, TeamNewsUpdate

router = APIRouter()


@router.get(
    "/{team_id}/news",
    response_model=list[TeamNewsResponse],
    dependencies=[AdminDeps],
    summary="Получение списка новостей команды",
)
async def get_team_news(team_id: int, team_news_service: TeamNewsServiceDeps) -> list[TeamNewsResponse]:
    return await team_news_service.get_news_all(team_id)


@router.post(
    "/{team_id}/news", response_model=TeamNewsResponse, dependencies=[AdminDeps], summary="Создание новости команды"
)
async def create_team(
    team_id: int, team_news_service: TeamNewsServiceDeps, news_data: TeamNewsCreate
) -> TeamNewsResponse:
    return await team_news_service.create_news(team_id, news_data)


@router.get(
    "/{team_id}/news/{id}",
    response_model=TeamNewsResponse,
    dependencies=[AdminDeps],
    summary="Получение одной новости команды по id",
)
async def get_team_news_item(team_id: int, id: int, team_news_service: TeamNewsServiceDeps) -> TeamNewsResponse:
    return await team_news_service.get_news(team_id, id)


@router.put(
    "/{team_id}/news{id}",
    response_model=TeamNewsResponse,
    dependencies=[AdminDeps],
    summary="Обновление данных новости команды",
)
async def update_team_news(
    team_news_service: TeamNewsServiceDeps, team_id: int, id: int, update_data: TeamNewsUpdate
) -> TeamNewsResponse:
    return await team_news_service.update_news(team_id, id, update_data)


@router.delete(
    "/{team_id}/news{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[AdminDeps],
    summary="Удаление данных новости команды",
)
async def delete_team_news(team_news_service: TeamNewsServiceDeps, team_id: int, id: int) -> None:
    await team_news_service.delete_news(team_id, id)
