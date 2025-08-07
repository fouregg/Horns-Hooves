from typing import Sequence

from sqlalchemy.orm import selectinload

from app.api.dto.organisation.request import OrganisationFilters
from app.db.models import Organisation, Activity
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

        if filters.name:
            conditions.append(Organisation.name.ilike(f"%{filters.name}%"))

        stmt = select(Organisation).where(*conditions)

        if filters.activity_name:
            stmt =stmt.join(Organisation.activities).where(
                Activity.name.ilike(f"%{filters.activity_name}%")
            )
            stmt = stmt.distinct()

        query = await self.session.execute(stmt)
        return query.scalars().all()