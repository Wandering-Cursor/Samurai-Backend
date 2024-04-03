import pydantic
from sqlmodel import Field

from samurai_backend.models.base import BaseModel


class AccountPermissionAccountLink(BaseModel, table=True):
    """
    Describes a permission that is assigned to an account.
    """

    account_permission_id: pydantic.UUID4 = Field(
        foreign_key="accountpermission.account_permission_id",
        primary_key=True,
    )
    account_id: pydantic.UUID4 = Field(
        foreign_key="accountmodel.account_id",
        primary_key=True,
    )
