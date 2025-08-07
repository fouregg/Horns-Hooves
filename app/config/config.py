from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class AuthConfig(_BaseSettings):
    AUTH_OPENAPI_USERNAME: str
    AUTH_OPENAPI_PASSWORD: str

    AUTH_TOKEN_TASK: str
    AUTH_CHECK_TELEGRAM_TOKEN: bool | None = True


class PostgresConfig(_BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_POOL_SIZE: int
    POSTGRES_MAX_OVERFLOW: int
    POSTGRES_ECHO: bool | None = None
    POSTGRES_ISOLATION_LEVEL: str = "READ COMMITTED"

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )



class LogsConfig(_BaseSettings):
    LOGS_IS_ENABLED: bool = True
    LOGS_LEVEL: str = "INFO"
    LOGS_IS_JSON: bool = True
    LOGS_OTLP_ENDPOINT: str | None = None
    LOGS_OTLP_TOKEN: str | None = None
    LOGS_OLTP_ENABLED: bool | None = False


class PrometheusConfig(_BaseSettings):
    PROMETHEUS_APP_NAME: str | None = Field(default="BackendAPI")
    PROMETHEUS_PREFIX: str | None = Field(default="fastapi")


class AlertsConfig(_BaseSettings):
    ALERTS_ENABLED: bool
    ALERTS_GRAFANA_URL: str
    ALERTS_GRAFANA_DATA_SOURCE: str
    ALERTS_CONTAINER_NAME: str

    ALERTS_TELEGRAM_BOT_API_URL: str | None = "https://api.telegram.org/bot"
    ALERTS_TELEGRAM_BOT_TOKEN: str
    ALERTS_TELEGRAM_CHAT_ID: int


class Config(_BaseSettings):
    auth: AuthConfig
    postgres: PostgresConfig
    logs: LogsConfig
    alerts: AlertsConfig
    prometheus: PrometheusConfig


def get_config() -> Config:
    return Config(
        auth=AuthConfig(),
        postgres=PostgresConfig(),
        logs=LogsConfig(),
        alerts=AlertsConfig(),
        prometheus=PrometheusConfig(),
    )
