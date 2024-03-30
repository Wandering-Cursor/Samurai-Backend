import pydantic
from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.account.schemas.account_details_mixin import AccountDetailsMixin
from samurai_backend.models.account.account import AccountModel

from .project import UserProjectModel


class UserProjectLinkRepresentation(AccountDetailsMixin):
    account_id: pydantic.UUID4

    @property
    def _account_id(self: "UserProjectLinkRepresentation") -> pydantic.UUID4:
        return self.account_id


class UserProjectLinkModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    account_id: pydantic.UUID4 = Field(foreign_key="accountmodel.account_id")
    user_project_id: pydantic.UUID4 = Field(foreign_key="userprojectmodel.project_id")

    account: AccountModel = Relationship(back_populates="user_project_links")
    user_project: UserProjectModel = Relationship(back_populates="account_links")
