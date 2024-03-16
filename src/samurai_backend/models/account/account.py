import secrets
import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.enums import AccountType
from samurai_backend.utils import get_password_hash

from .account_permission_link import AccountPermissionAccountLink
from .connection_link import ConnectionLinkModel

if TYPE_CHECKING:
    from .account_permission import AccountPermission
    from .connection import ConnectionModel
    from .registration_code import RegistrationEmailCode


def registration_code_generator() -> str:
    return "samurai-" + secrets.token_urlsafe(12)


def username_generator() -> str:
    return f"samurai-{secrets.token_urlsafe(12)}"


def email_generator() -> str:
    return f"{secrets.token_urlsafe(12)}@samurai.com"


def salt_generator() -> str:
    return secrets.token_urlsafe(32)


def default_account_type() -> AccountType:
    return AccountType.STUDENT


def default_password_generator() -> str:
    return secrets.token_urlsafe(64)


class BaseAccountModel(SQLModel):
    account_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        description="The unique identifier for the account. Has a default value of a new UUID4.",
    )

    email: str = Field(
        default_factory=email_generator,
        unique=True,
        index=True,
        max_length=512,
        description="If not provided, a random email will be generated.",
    )
    username: str = Field(
        default_factory=username_generator,
        unique=True,
        index=True,
        max_length=128,
    )
    account_type: AccountType = Field(
        default_factory=default_account_type,
    )

    first_name: str = Field(max_length=256)
    middle_name: str | None = Field(default=None, nullable=True, max_length=256)
    last_name: str = Field(max_length=256)

    registration_code: str = Field(
        default_factory=registration_code_generator,
        nullable=True,
    )

    is_active: bool = Field(default=True)
    is_email_verified: bool = Field(default=False)


class CreateAccountModel(BaseAccountModel):
    password: str = Field(
        default_factory=default_password_generator,
        max_length=512,
    )

    permissions: list[pydantic.UUID4]
    connections: list[pydantic.UUID4]


class AccountModel(BaseAccountModel, table=True):
    salt: str = Field(
        default_factory=salt_generator,
    )
    hashed_password: str

    permissions: list["AccountPermission"] = Relationship(
        back_populates="accounts",
        link_model=AccountPermissionAccountLink,
    )
    connections: list["ConnectionModel"] = Relationship(
        back_populates="account",
        link_model=ConnectionLinkModel,
    )
    registration_email_code: "RegistrationEmailCode" = Relationship(
        back_populates="account",
    )

    def set_password(self: "AccountModel", password: str) -> None:
        if not self.salt:
            self.salt = salt_generator()

        self.hashed_password = get_password_hash(self.salt, password)

    @classmethod
    def from_create_model(cls: "AccountModel", account: CreateAccountModel) -> "AccountModel":
        obj = cls(
            account_id=account.account_id,
            email=account.email,
            username=account.username,
            account_type=account.account_type,
            first_name=account.first_name,
            middle_name=account.middle_name,
            last_name=account.last_name,
            registration_code=account.registration_code,
            is_active=account.is_active,
            is_email_verified=account.is_email_verified,
        )
        obj.set_password(account.password)

        return obj
