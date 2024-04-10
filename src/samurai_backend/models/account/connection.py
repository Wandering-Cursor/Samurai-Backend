import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from samurai_backend.models.base import BaseModel

from .connection_link import ConnectionLinkModel

if TYPE_CHECKING:
    from .account import AccountModel


class ConnectionCreate(BaseModel):
    group_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="groupmodel.group_id",
        nullable=True,
    )
    faculty_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="facultymodel.faculty_id",
        nullable=True,
    )
    department_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="departmentmodel.department_id",
        nullable=True,
    )


class ConnectionBase(ConnectionCreate):
    connection_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )


class ConnectionModel(ConnectionBase, table=True):
    accounts: list["AccountModel"] = Relationship(
        back_populates="connections",
        link_model=ConnectionLinkModel,
    )
