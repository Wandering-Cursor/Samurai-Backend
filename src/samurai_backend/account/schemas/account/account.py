import pydantic

from samurai_backend.account.schemas.account.account_representation import AccountRepresentation
from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.enums import AccountType


class VerboseAccountRepresentation(AccountRepresentation):
    is_active: bool

    account_type: AccountType


class AdminAccountRepresentation(VerboseAccountRepresentation):
    is_email_verified: bool
    registration_code: str | None

    salt: str
    hashed_password: str


class AccountSearchSchema(pydantic.BaseModel):
    account_id: pydantic.UUID4 | None = None
    email: pydantic.EmailStr | None = None
    username: str | None = None

    account_type: AccountType | None = None

    registration_code: str | None = None


class AccountSearchPaginationSchema(AccountSearchSchema, PaginationSearchSchema):
    pass


class AccountSearchResultVerbose(BasePaginatedResponse):
    content: list[VerboseAccountRepresentation]


class AccountSetPermissionsInput(pydantic.BaseModel):
    permissions: list[pydantic.UUID4]
