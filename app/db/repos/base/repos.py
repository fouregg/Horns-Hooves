from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Organisation
from app.db.repos.activity import ActivityRepo
from app.db.repos.organisation import OrganisationRepo
from app.db.repos.task import TaskRepo


class Repos:
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def task(self) -> TaskRepo:
        return TaskRepo(session=self.session)

    @property
    def organisation(self) -> OrganisationRepo:
        return OrganisationRepo(session=self.session)

    @property
    def activity(self) -> ActivityRepo:
        return ActivityRepo(session=self.session)
