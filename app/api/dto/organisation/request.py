from typing import Optional

from app.init.base_models import BaseModel
from fastapi import Query

class OrganisationFilters(BaseModel):
    activity_name: Optional[str] = Query(default=None, description="Название деятельности")
    name: Optional[str] = Query(default=None, description="Название организации")
