from datetime import date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.events import Event
from app.repositories.event_repo import EventRepository
from app.schemas.calendar import CalendarDayResponse, CalendarMonthResponse, EventOut, YearMonthParams
from app.schemas.users import User


class CalendarService:
    """Сервис для управления событиями"""

    def __init__(self, session: AsyncSession):
        self.repo = EventRepository(session)

    def grouping_events_by_day(self, events: list[Event]) -> dict[str, list[EventOut]]:
        """Группировка событий по дням"""
        calendar = {}
        for event in events:
            date = event.start_time.date().isoformat()
            calendar.setdefault(date, []).append(EventOut.model_validate(event))
        return calendar

    def get_month_bounds(self, year: int, month: int) -> tuple[datetime, datetime]:
        """Получение дат начала и конца месяца"""
        start_date = datetime(year, month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1)
        return start_date, end_date

    async def get_monthly_events(self, params: YearMonthParams, user: User) -> list[CalendarMonthResponse]:
        """Получение события за определенный месяц"""
        start_date, end_date = self.get_month_bounds(params.year, params.month)
        events = await self.repo.get_by_period(user.id, start_date, end_date)
        calendar = self.grouping_events_by_day(events)
        return [CalendarMonthResponse(date=date, events=events) for date, events in sorted(calendar.items())]

    async def get_daily_events(self, date: date, user: User) -> list[Event]:
        """Получение события за определенный день"""
        start_date = date
        end_date = start_date + timedelta(days=1)
        events = await self.repo.get_by_period(user.id, start_date, end_date)
        return CalendarDayResponse(events=[EventOut.model_validate(e) for e in events])
