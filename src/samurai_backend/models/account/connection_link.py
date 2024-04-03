import pydantic
from sqlmodel import Field

from samurai_backend.models.base import BaseModel


class ConnectionLinkModel(BaseModel, table=True):
    account_id: pydantic.UUID4 = Field(
        foreign_key="accountmodel.account_id",
        primary_key=True,
    )
    connection_id: pydantic.UUID4 = Field(
        foreign_key="connectionmodel.connection_id",
        primary_key=True,
    )
