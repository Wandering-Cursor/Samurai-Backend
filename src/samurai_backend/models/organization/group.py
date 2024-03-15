import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .faculty import FacultyModel


class GroupModel(SQLModel, table=True):
    """
    Group is the lowest level of organization in an educational institution.
    Groups are sub-units of faculties.

    Each student is assigned to one of the groups.
    """

    group_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )
    faculty_id: pydantic.UUID4 = Field(
        foreign_key="facultymodel.faculty_id",
    )

    name: str
    description: str | None = Field(
        default=None,
        nullable=True,
    )

    faculty: "FacultyModel" = Relationship(back_populates="groups")
