from app.models import EmployeeManagers
from app.repositories.base_repository import BaseRepository


class EmployeeManagerRepository(BaseRepository):
    """Репозиторий для управления менеджерами отделов"""

    model: type[EmployeeManagers] = EmployeeManagers
