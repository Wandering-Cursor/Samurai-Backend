from math import ceil

import pydantic

from samurai_backend.settings import security_settings


class BaseSchema(pydantic.BaseModel):
    class Config:
        from_attributes = True


class ErrorSchema(pydantic.BaseModel):
    detail: str


class GetToken(pydantic.BaseModel):
    username: str
    password: str
    access_token_ttl_min: int | None = pydantic.Field(
        default=None,
        description="The time-to-live of the access token in minutes. (Optional)",
        ge=1,
        le=security_settings.access_token_lifetime_minutes,
    )


class RefreshTokenInput(pydantic.BaseModel):
    refresh_token: str | None = None


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    sub: pydantic.UUID4 = pydantic.Field(alias="sub")
    scopes: list[str] = []
    type: str = "access"


class PaginationSearchSchema(pydantic.BaseModel):
    page: int = pydantic.Field(
        default=1,
        ge=1,
    )
    page_size: int = pydantic.Field(
        default=10,
        ge=1,
    )

    @property
    def search_page(self: "PaginationSearchSchema") -> int:
        return self.page - 1


class PaginationMetaInformation(pydantic.BaseModel):
    total: int

    page: int
    page_size: int

    @pydantic.computed_field
    @property
    def total_pages(self) -> int:
        return ceil(self.total / self.page_size)


class BasePaginatedResponse(pydantic.BaseModel):
    meta: PaginationMetaInformation
    content: list
