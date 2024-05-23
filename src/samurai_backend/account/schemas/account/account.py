import pydantic

from samurai_backend.account.schemas.account.account_representation import AccountRepresentation
from samurai_backend.enums.account_type import AccountType
from samurai_backend.errors import SamuraiInvalidRequestError
from samurai_backend.schemas import BasePaginatedResponse, PaginationSearchSchema


class VerboseAccountRepresentation(
    AccountRepresentation,
):
    is_active: bool

    account_type: AccountType

    class Config:
        from_attributes = True


class AdminAccountRepresentation(
    VerboseAccountRepresentation,
):
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


class AccountCreateConnectionForBatch(pydantic.BaseModel):
    group_id: pydantic.UUID4 | None = None
    faculty_id: pydantic.UUID4 | None = None
    department_id: pydantic.UUID4 | None = None


class AccountCreateInputForBatch(pydantic.BaseModel):
    account_type: AccountType = AccountType.STUDENT

    first_name: str = pydantic.Field(max_length=256)
    middle_name: str | None = pydantic.Field(default=None, max_length=256)
    last_name: str = pydantic.Field(max_length=256)

    is_email_verified: bool = False

    connections: list[AccountCreateConnectionForBatch] = pydantic.Field(default_factory=list)
    permissions: list[pydantic.UUID4] = pydantic.Field(default_factory=list)

    class Config:
        from_attributes = True


class AccountBatchCreateInput(pydantic.BaseModel):
    accounts: list[AccountCreateInputForBatch]


class AccountBatchCreateOutput(pydantic.BaseModel):
    status: str = "success"
