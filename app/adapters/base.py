from app.adapters.alerts import AlertsAdapter
from app.config.config import Config
from app.external.base.aiohttp_client import AioHttpClient


class Adapters:
    def __init__(self, config: Config):
        self.config = config
        self.alerts = AlertsAdapter(config=config)
        self.http_client = AioHttpClient(auth_header={}, base_url="")
