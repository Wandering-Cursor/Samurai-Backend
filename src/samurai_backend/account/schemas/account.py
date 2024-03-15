import pydantic

from samurai_backend.core.schemas import BaseSchema


class BaseAccount(BaseSchema):
    account_id: pydantic.UUID4
    email: pydantic.EmailStr


class AccountRepresentation(BaseAccount):
    username: str

    first_name: str
    middle_name: str | None = None
    last_name: str


class VerboseAccountRepresentation(AccountRepresentation):
    is_active: bool


class AdminAccountRepresentation(VerboseAccountRepresentation):
    is_email_verified: bool
    registration_code: str | None

    salt: str
    hashed_password: str


AccountSchema = AdminAccountRepresentation


class AccountSearchSchema(pydantic.BaseModel):
    account_id: pydantic.UUID4 | None = None
    email: pydantic.EmailStr | None = None
    username: str | None = None
