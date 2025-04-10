from app.models import Division
from app.repositories.base_repository import BaseRepository


class DivisionRepository(BaseRepository):
    model = Division
