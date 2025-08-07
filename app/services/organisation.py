import math
from collections import defaultdict
from http import HTTPStatus

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
from app.api.exceptions import ClientError
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
        if result is None:
            raise ClientError(status_code=HTTPStatus.NOT_FOUND, message="Не существует организации с таким id")
        return ShortOrganisation(name=result.name, activities=[activity.name for activity in result.activities])

    async def get_organization_by_building(self, building_id: int) -> List[ShortOrganisation]:
        results = await self.repo.get_organisation_by_building(building_id=building_id)
        if results is None:
            raise ClientError(status_code=HTTPStatus.NOT_FOUND, message="Не существует организации в заднии с таким id или не существует здания")
        response = []
        for el in results:
            tmp = await self.repos.activity.get_activity_by_organisation(el.id)
            response.append(ShortOrganisation(name=el.name, activities=[activity.name for activity in tmp]))
        return response

    async def get_organisations(self, filters: OrganisationFilters) -> List[ShortOrganisation]:
        results = await self.repo.get_organisations(filters=filters)
        if filters.limit_longitude and filters.limit_latitude and (not filters.point_longitude or not filters.point_longitude):
            raise ClientError(status_code=HTTPStatus.BAD_REQUEST, message="Введены ограничения, но не задана точка")
        elif filters.point_longitude and filters.point_longitude and (not filters.limit_longitude or not filters.limit_latitude):
            raise ClientError(status_code=HTTPStatus.BAD_REQUEST, message="Введена точка, но не введены ограничения")

        response = []
        for el in results:
            tmp = await self.repos.activity.get_activity_by_organisation(el.id)
            response.append(ShortOrganisation(name=el.name, activities=[activity.name for activity in tmp]))
        return response