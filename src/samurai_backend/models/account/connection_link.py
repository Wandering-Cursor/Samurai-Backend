import pydantic
from sqlmodel import Field, SQLModel


class ConnectionLinkModel(SQLModel, table=True):
    account_id: pydantic.UUID4 = Field(
        foreign_key="accountmodel.account_id",
        primary_key=True,
    )
    connection_id: pydantic.UUID4 = Field(
        foreign_key="connectionmodel.connection_id",
        primary_key=True,
    )
