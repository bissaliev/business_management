from app.models import Department
from app.repositories.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    model = Department
