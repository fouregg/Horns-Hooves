from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repos.base.base import BaseRepo


class TaskRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)
