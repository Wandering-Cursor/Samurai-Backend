import pydantic
from sqlmodel import Field, SQLModel


class AccountPermissionAccountLink(SQLModel, table=True):
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
