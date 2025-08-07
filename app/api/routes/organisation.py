from typing import Annotated, List

from fastapi import APIRouter, Depends
from openpyxl.worksheet.filters import Filters
from starlette import status

from app.api.dto.organisation.request import OrganisationFilters
from app.api.dto.organisation.responce import ShortOrganisation
from app.services.organisation import OrganisationService
from app.services.task import TaskService

router = APIRouter(tags=["Организация"])


@router.get(
    path="/organisation/{organisation_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShortOrganisation,
    description="Получение всех организаций в здании",
)
async def get_organisation(
        organisation_id: int,
        organisation_service: Annotated[OrganisationService, Depends()]
) -> ShortOrganisation:
    return await organisation_service.get_organisation(organisation_id=organisation_id)

@router.get(
    path="/organisation/{building_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[ShortOrganisation],
    description="Получение всех организаций в здании",
)
async def get_organization_by_building(
        building_id: int,
        organisation_service: Annotated[OrganisationService, Depends()]
) -> List[ShortOrganisation]:
    """Получение всех организаций в здании"""
    return await organisation_service.get_organization_by_building(building_id=building_id)

@router.get(
    path="/organisations",
    status_code=status.HTTP_200_OK,
    response_model=List[ShortOrganisation],
    description="Получение всех организаций с фильтрами",
)
async def get_organizations(
        filters: Annotated[OrganisationFilters, Depends()],
        organisation_service: Annotated[OrganisationService, Depends()]
) -> List[ShortOrganisation]:
    """Получение всех организаций в здании"""
    return await organisation_service.get_organisations(filters=filters)