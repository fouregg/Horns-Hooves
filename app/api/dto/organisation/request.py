from typing import Optional

from app.init.base_models import BaseModel
from fastapi import Query

class OrganisationFilters(BaseModel):
    activity_name: Optional[str] = Query(default=None, description="Название деятельности")
    name: Optional[str] = Query(default=None, description="Название организации")
    limit_latitude: Optional[float] = Query(default=None, description="Ограничение по широте")
    limit_longitude: Optional[float] = Query(default=None, description="Ограничение по долготе")
    point_latitude: Optional[float]= Query(default=None, description="Широта точки откуда идет ограничение")
    point_longitude: Optional[float] = Query(default=None, description="Долгота точки откуда идет ограничение")
