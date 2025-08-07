import math
from collections import defaultdict

from typing import Annotated, List

import structlog
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.adapters.base import Adapters
from app.api.dependencies.stubs import (
    dependency_adapters,
    dependency_session_factory,
    placeholder,
)
from app.api.dto.organisation.request import OrganisationFilters
from app.api.dto.organisation.responce import ShortOrganisation
from app.db.models import Organisation
from app.services.base.base import BaseService


logger = structlog.stdlib.get_logger()


class OrganisationService(BaseService):
    def __init__(
        self,
        adapters: Annotated[Adapters, Depends(dependency_adapters)],
        session_factory: Annotated[sessionmaker, Depends(dependency_session_factory)],
        session: Annotated[AsyncSession, Depends(placeholder)] = None,
    ):
        super().__init__(session_factory=session_factory, adapters=adapters, session=session)
        self.adapters = adapters
        self.repo = self.repos.organisation

    async def get_organisation(self, organisation_id: int) -> ShortOrganisation:
        result = await self.repo.get_organisation(organisation_id=organisation_id)
        return ShortOrganisation(name=result.name, activities=[activity.name for activity in result.activities])

    async def get_organization_by_building(self, building_id: int) -> List[ShortOrganisation]:
        results = await self.repo.get_organisation_by_building(building_id=building_id)
        response = []
        for el in results:
            tmp = await self.repos.activity.get_activity_by_organisation(el.id)
            response.append(ShortOrganisation(name=el.name, activities=[activity.name for activity in tmp]))
        return response

    async def get_organisations(self, filters: OrganisationFilters) -> List[ShortOrganisation]:
        results = await self.repo.get_organisations(filters=filters)
        response = []
        for el in results:
            tmp = await self.repos.activity.get_activity_by_organisation(el.id)
            response.append(ShortOrganisation(name=el.name, activities=[activity.name for activity in tmp]))
        return response