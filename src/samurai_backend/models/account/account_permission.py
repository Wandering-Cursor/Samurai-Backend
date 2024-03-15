import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

from .account_permission_link import AccountPermissionAccountLink

if TYPE_CHECKING:
    from .account import AccountModel


class AccountPermission(SQLModel, table=True):
    """
    Describes a permission that can be assigned to an account.
    """

    account_permission_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    name: str = Field(unique=True, index=True)
    description: str = Field(default="No description")

    accounts: list["AccountModel"] = Relationship(
        back_populates="permissions",
        link_model=AccountPermissionAccountLink,
    )
