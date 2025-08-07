from pydantic import Field

from app.init.base_models import BaseModel


class WebappData(BaseModel):
    telegram_id: int
    language_code: str | None = Field(default="ru")
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_premium: bool | None = None
    photo_url: str | None = None
    start_param: str | None = None


class MenuParamsDTO(BaseModel):
    has_lunches: bool = False
    is_admin: bool = False


class JWToken(BaseModel):
    id: int
    role: str
    expires: str
