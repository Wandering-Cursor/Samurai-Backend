import pydantic
import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.models.account.account import AccountModel

from .project import UserProjectModel


class UserProjectLinkModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    account_id: pydantic.UUID4 = Field(
        sa_column=sa.Column(
            sa.UUID(),
            sa.ForeignKey("accountmodel.account_id", ondelete="CASCADE"),
            index=True,
        ),
    )
    user_project_id: pydantic.UUID4 = Field(
        sa_column=sa.Column(
            sa.UUID(),
            sa.ForeignKey("userprojectmodel.project_id", ondelete="CASCADE"),
            index=True,
        )
    )

    account: AccountModel = Relationship(back_populates="user_project_links")
    user_project: UserProjectModel = Relationship(back_populates="account_links")
