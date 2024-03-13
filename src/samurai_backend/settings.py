from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "postgresql://local:local@127.0.0.1:5432/DevDB"

    class Config:
        env_prefix = "app_"


class SecuritySettings(BaseSettings):
    secret_key: str = "secret_jwt_key"
    cors_allow_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    class Config:
        env_prefix = "security_"


settings = Settings(_env_file="settings.env", _env_file_encoding="UTF-8")
security_settings = SecuritySettings(_env_file="security.env", _env_file_encoding="UTF-8")
