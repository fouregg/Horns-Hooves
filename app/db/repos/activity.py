from typing import Sequence

from app.db.models import Organisation, Activity
from app.db.repos.base.base import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

class ActivityRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_activity_by_organisation(self, organisation_id: int) -> Sequence[Activity]:
        stmt = select(Activity).where(Activity.organization_id == organisation_id)
        query = await self.session.execute(stmt)
        return query.scalars().all()
