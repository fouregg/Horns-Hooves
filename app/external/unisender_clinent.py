import structlog
from aiohttp import ClientResponse

from app.api.dto.base import SuccessResponse
from app.config.config import Config
from app.external.base.aiohttp_client import AioHttpClient
from typing import Optional

logger = structlog.stdlib.get_logger()


class UnisenderClient:
    def __init__(self, config: Config):
        self.config = config

        self.http_client = AioHttpClient(
            auth_header={},
            base_url=self.config.email.UNISENDER_API_URL,
        )

    async def send_email(self, email: str, reset_link: str) -> ClientResponse:
        subject = "Восстановление пароля"
        body = f"""
             <p>Для сброса пароля перейдите по ссылке:</p>
             <p><a href="{reset_link}">Сбросить пароль</a></p>
             <p>Ссылка действительна в течение 1 часа.</p>
             """

        payload = {
            "format": "json",
            "api_key": self.config.email.UNISENDER_API_KEY,
            "email": email,
            "sender_name": self.config.email.EMAIL_FROM_NAME,
            "sender_email": self.config.email.EMAIL_FROM,
            "subject": subject,
            "body": body,
            "lang": "ru",
            "list_id": self.config.email.UNISENDER_LIST_ID,
        }

        resp = await self.http_client.request(
            url="",
            method="GET",
            params=payload,
        )

        return resp
