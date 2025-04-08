from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.structure_services import OrgStructureService


async def org_structure_service(session: Annotated[AsyncSession, Depends(get_session)]):
    return OrgStructureService(session)


OrgStructureServiceDeps = Annotated[OrgStructureService, Depends(org_structure_service)]
