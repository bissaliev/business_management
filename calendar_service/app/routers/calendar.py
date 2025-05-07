from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from app.routers.dependencies import CalendarServiceDeps, CurrentUser
from app.schemas.calendar import CalendarDayResponse, CalendarMonthResponse, YearMonthParams

router = APIRouter()


@router.get("/month", response_model=list[CalendarMonthResponse])
async def get_monthly_calendar(
    params: Annotated[YearMonthParams, Depends()], user: CurrentUser, calendar_service: CalendarServiceDeps
) -> list[CalendarMonthResponse]:
    calendar = await calendar_service.get_monthly_events(params, user)
    return calendar


@router.get("/day", response_model=CalendarDayResponse)
async def get_daily_calendar(
    date: date, user: CurrentUser, calendar_service: CalendarServiceDeps
) -> CalendarDayResponse:
    return await calendar_service.get_daily_events(date, user)
