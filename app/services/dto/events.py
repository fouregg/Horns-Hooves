import datetime

from app.init.base_models import BaseModel


class EventDTO(BaseModel):
    external_id: str
    location: str
    datetime: datetime.datetime
    checkpoint: str
    area: str
    fio: str
