from app.models.teams import Team
from app.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository):
    """Репозиторий команд"""

    model = Team
