import pytz
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    database_url: str = "postgresql://local:local@127.0.0.1:5432/DevDB"
    timezone_name: str = "UTC"
    script_nonce: str = "FakeNonce"

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
