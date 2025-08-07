from typing import Sequence

from sqlalchemy.orm import selectinload

from app.api.dto.organisation.request import OrganisationFilters
from app.db.models import Organisation, Activity, Building
from app.db.repos.base.base import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

class OrganisationRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_organisation(self, organisation_id: int) -> Organisation:
        stmt = select(Organisation).options(selectinload(Organisation.activities)).where(Organisation.id == organisation_id)
        query = await self.session.execute(stmt)
        return query.scalar_one_or_none()

    async def get_organisation_by_building(self, building_id: int) -> Sequence[Organisation]:
        stmt = select(Organisation).where(Organisation.building_id == building_id)
        query = await self.session.execute(stmt)
        return query.scalars().all()

    async def get_organisations(self, filters: OrganisationFilters) -> Sequence[Organisation]:
        conditions = []

        stmt = select(Organisation)

        if filters.name:
            conditions.append(Organisation.name.ilike(f"%{filters.name}%"))

        if filters.activity_name:
            stmt =stmt.join(Organisation.activities).where(
                Activity.name.ilike(f"%{filters.activity_name}%")
            )
            stmt = stmt.distinct()

        if all([filters.point_latitude, filters.point_longitude,
                filters.limit_latitude, filters.limit_longitude]):
            stmt = stmt.join(Organisation.building)

            min_lat = filters.point_latitude - filters.limit_latitude
            max_lat = filters.point_latitude + filters.limit_latitude
            min_lon = filters.point_longitude - filters.limit_longitude
            max_lon = filters.point_longitude + filters.limit_longitude

            conditions.extend([
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon)
            ])

        stmt = stmt.where(*conditions)

        query = await self.session.execute(stmt)
        return query.scalars().all()