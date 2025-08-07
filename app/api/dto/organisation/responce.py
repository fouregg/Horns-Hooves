from app.api.dto.base import BaseResponse


class ShortOrganisation(BaseResponse):
    name: str
    activities: list[str]
