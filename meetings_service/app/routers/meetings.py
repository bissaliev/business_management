from fastapi import APIRouter, status

from app.routers.dependencies import CurrentUser, MeetingServiceDeps
from app.schemas.meeting import MeetingCreate, MeetingOut, MeetingParticipantOut, MeetingUpdate, Participant

router = APIRouter()


@router.post("/", response_model=MeetingOut, summary="Создание встречи")
async def create_meeting(
    meeting_data: MeetingCreate, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> MeetingOut:
    meeting = await meeting_service.create_meeting(user, meeting_data)

    return meeting


@router.get("/", response_model=list[MeetingParticipantOut], summary="Список встреч текущего пользователя")
async def list_meetings(
    user: CurrentUser, meeting_service: MeetingServiceDeps, team_id: int | None = None
) -> list[MeetingParticipantOut]:
    meetings = await meeting_service.get_list_meetings(user, team_id)
    return meetings


@router.get("/{meeting_id}", response_model=MeetingParticipantOut, summary="Поучение встречи")
async def get_meeting(
    meeting_id: int, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> MeetingParticipantOut:
    meeting = await meeting_service.get_meeting(user, meeting_id)
    return meeting


@router.put("/{meeting_id}", response_model=MeetingOut, summary="Обновление данных встречи")
async def update_meeting(
    meeting_id: int, user: CurrentUser, update_data: MeetingUpdate, meeting_service: MeetingServiceDeps
) -> MeetingOut:
    meeting = await meeting_service.update_meeting(user, meeting_id, update_data)
    return meeting


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Отмена встречи")
async def delete_meeting(meeting_id: int, user: CurrentUser, meeting_service: MeetingServiceDeps):
    await meeting_service.delete_meeting(user, meeting_id)


@router.post(
    "/{meeting_id}/participants/", status_code=status.HTTP_204_NO_CONTENT, summary="Добавление участника встречи"
)
async def add_participant(
    meeting_id: int, user: CurrentUser, participant: Participant, meeting_service: MeetingServiceDeps
) -> None:
    await meeting_service.add_participant(meeting_id, participant, user)


@router.delete(
    "/{meeting_id}/participants/{participant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление участника встречи",
)
async def delete_participant(
    meeting_id: int, participant_id: int, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> None:
    await meeting_service.delete_participant(meeting_id, participant_id, user)
