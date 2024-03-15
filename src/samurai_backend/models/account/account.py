import secrets
import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.utils import get_password_hash

from .account_permission_link import AccountPermissionAccountLink
from .connection_link import ConnectionLinkModel

if TYPE_CHECKING:
    from .account_permission import AccountPermission
    from .connection import ConnectionModel


def registration_code_generator() -> str:
    return "samurai-" + secrets.token_urlsafe(12)


def email_generator() -> str:
    return secrets.token_urlsafe(12) + "@samurai.com"


def salt_generator() -> str:
    return secrets.token_urlsafe(32)


class BaseAccountModel(SQLModel):
    account_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    email: str = Field(
        default_factory=email_generator,
        unique=True,
        index=True,
        max_length=512,
    )
    username: str = Field(
        unique=True,
        index=True,
        max_length=128,
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


class AccountModel(BaseAccountModel, table=True):
    salt: str = Field(default_factory=salt_generator)
    hashed_password: str

    permissions: list["AccountPermission"] = Relationship(
        back_populates="accounts",
        link_model=AccountPermissionAccountLink,
    )
    connections: list["ConnectionModel"] = Relationship(
        back_populates="account",
        link_model=ConnectionLinkModel,
    )

    def set_password(self: "AccountModel", password: str) -> None:
        if not self.salt:
            self.salt = salt_generator()

        self.hashed_password = get_password_hash(self.salt, password)
