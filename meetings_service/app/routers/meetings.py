from fastapi import APIRouter

from app.routers.dependencies import CurrentUser, MeetingServiceDeps
from app.schemas.meeting import MeetingCreate, MeetingOut, MeetingParticipantOut, MeetingUpdate, Participant
from app.schemas.responses import MessageMeetingDelete, MessageParticipantAdd, MessageParticipantDelete

router = APIRouter()


@router.post("/", summary="Создание встречи")
async def create_meeting(
    meeting_data: MeetingCreate, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> MeetingOut:
    meeting = await meeting_service.create_meeting(user, meeting_data)

    return meeting


@router.get("/", summary="Список встреч текущего пользователя")
async def list_meetings(
    user: CurrentUser, meeting_service: MeetingServiceDeps, team_id: int | None = None
) -> list[MeetingParticipantOut]:
    meetings = await meeting_service.get_list_meetings(user, team_id)
    return meetings


@router.get("/{meeting_id}", summary="Поучение встречи")
async def get_meeting(
    meeting_id: int, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> MeetingParticipantOut:
    meeting = await meeting_service.get_meeting(user, meeting_id)
    return meeting


@router.put("/{meeting_id}", summary="Обновление данных встречи")
async def update_meeting(
    meeting_id: int, user: CurrentUser, update_data: MeetingUpdate, meeting_service: MeetingServiceDeps
) -> MeetingOut:
    meeting = await meeting_service.update_meeting(user, meeting_id, update_data)
    return meeting


@router.delete("/{meeting_id}", summary="Отмена встречи")
async def delete_meeting(
    meeting_id: int, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> MessageMeetingDelete:
    await meeting_service.delete_meeting(user, meeting_id)
    return MessageMeetingDelete()


@router.post("/{meeting_id}/participants/", summary="Добавление участника встречи")
async def add_participant(
    meeting_id: int, user: CurrentUser, participant: Participant, meeting_service: MeetingServiceDeps
) -> MessageParticipantAdd:
    await meeting_service.add_participant(meeting_id, participant, user)
    return MessageParticipantAdd()


@router.delete("/{meeting_id}/participants/{participant_id}", summary="Удаление участника встречи")
async def delete_participant(
    meeting_id: int, participant_id: int, user: CurrentUser, meeting_service: MeetingServiceDeps
) -> MessageParticipantDelete:
    await meeting_service.delete_participant(meeting_id, participant_id, user)
    return MessageParticipantDelete()
