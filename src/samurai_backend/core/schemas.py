import pydantic

from samurai_backend.settings import security_settings


class BaseSchema(pydantic.BaseModel):
    class Config:
        from_attributes = True


class GetToken(pydantic.BaseModel):
    username: str
    password: str
    access_token_ttl_min: int | None = pydantic.Field(
        default=None,
        description="The time-to-live of the access token in minutes. (Optional)",
        ge=1,
        le=security_settings.access_token_lifetime_minutes,
    )


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    account_id: pydantic.UUID4
    scopes: list[str] = []
