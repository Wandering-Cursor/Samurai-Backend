import pydantic

from samurai_backend.account.schemas.account.account_representation import AccountRepresentation
from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.enums import AccountType
from samurai_backend.errors import SamuraiInvalidRequestError


class VerboseAccountRepresentation(AccountRepresentation):
    is_active: bool

    account_type: AccountType

    class Config:
        from_attributes = True


class AdminAccountRepresentation(VerboseAccountRepresentation):
    is_email_verified: bool
    registration_code: str | None

    salt: str
    hashed_password: str


class AccountSearchSchema(pydantic.BaseModel):
    account_id: pydantic.UUID4 | None = None
    email: str | None = None
    username: str | None = None

    account_type: AccountType | None = None

    registration_code: str | None = None


class AccountSearchPaginationSchema(AccountSearchSchema, PaginationSearchSchema):
    pass


class AccountSearchResultVerbose(BasePaginatedResponse):
    content: list[VerboseAccountRepresentation]


class AccountSetPermissionsInput(pydantic.BaseModel):
    permissions: list[pydantic.UUID4]


class AccountSetConnectionsInput(pydantic.BaseModel):
    connections: list[pydantic.UUID4]


class AccountSimpleSearchSchema(pydantic.BaseModel):
    account_id: pydantic.UUID4 | None = None
    email: str | None = None
    username: str | None = None

    @pydantic.model_validator(mode="after")
    def validate_model(self: "AccountSimpleSearchSchema") -> "AccountSimpleSearchSchema":
        if not any([self.account_id, self.email, self.username]):
            raise SamuraiInvalidRequestError("At least one search parameter must be provided.")
        return self
