import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.enums import Permissions

from .account_permission_link import AccountPermissionAccountLink

if TYPE_CHECKING:
    from .account import AccountModel


class CreatePermission(SQLModel):
    name: Permissions = Field(unique=True, index=True)
    description: str = Field(default="No description")


class PermissionBase(CreatePermission):
    """
    Describes a permission that can be assigned to an account.
    """

    account_permission_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )


class AccountPermission(PermissionBase, table=True):
    name: str = Field(unique=True, index=True)

    accounts: list["AccountModel"] = Relationship(
        back_populates="permissions",
        link_model=AccountPermissionAccountLink,
    )
