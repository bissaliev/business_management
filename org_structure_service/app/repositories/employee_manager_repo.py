from app.models import EmployeeManagers
from app.repositories.base_repository import BaseRepository


class EmployeeManagerRepository(BaseRepository):
    model = EmployeeManagers
