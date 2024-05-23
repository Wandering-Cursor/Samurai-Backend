from importlib import metadata

import pytz
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    app_version: str = metadata.version("samurai_backend")
    database_url: str = "postgresql+psycopg://local:local@127.0.0.1:5432/DevDB"
    timezone_name: str = "UTC"
    script_nonce: str = "FakeNonce"
    logging_level: str = "DEBUG"
    events_logging_level: str = "DEBUG"
    email_service_api_key: str | None = None

    email_registration_code_template_id: int = 1
    email_reset_password_code_template_id: int = 2
    email_password_changed_template_id: int = 3

    otel_exporter_endpoint: str = "http://localhost:4318/v1/traces"
    otel_auth_header: str | None = None

    @property
    def timezone(self) -> pytz.BaseTzInfo:
        return pytz.timezone(self.timezone_name)

    class Config:
        env_prefix = "app_"


class SecuritySettings(BaseSettings):
    secret_key: str = "secret_jwt_key"
    algorithm: str = "HS256"
    access_token_lifetime_minutes: int = 30
    refresh_token_lifetime_minutes: int = 60 * 24 * 7
    max_access_token_ttl: int = 60 * 24 * 31
    cookie_domain: str = ".obscurial.art"

    cors_allow_origins: list[str] = []
    cors_allow_origin_regex: str = r"(((http|https):\/\/)?localhost.*)"
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    class Config:
        env_prefix = "security_"


settings = Settings(
    _env_file="/run/secrets/settings_env",
    _env_file_encoding="UTF-8",
)
security_settings = SecuritySettings(
    _env_file="/run/secrets/security_env",
    _env_file_encoding="UTF-8",
)
