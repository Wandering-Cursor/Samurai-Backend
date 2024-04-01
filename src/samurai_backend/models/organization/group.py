import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from .faculty import FacultyModel


class GroupCreate(SQLModel):
    faculty_id: pydantic.UUID4 = Field(
        foreign_key="facultymodel.faculty_id",
    )

    name: str
    description: str | None = Field(
        default=None,
        nullable=True,
    )


class Group(GroupCreate):
    group_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )


class GroupRepresentation(Group):
    @pydantic.computed_field
    @property
    def _links(self) -> dict[str, dict[str, str]]:
        return {
            "self": {"href": f"/admin/group/{self.group_id}"},
            "faculty": {"href": f"/admin/faculty/{self.faculty_id}"},
        }


class GroupModel(Group, table=True):
    """
    Group is the lowest level of organization in an educational institution.
    Groups are sub-units of faculties.

    Each student is assigned to one of the groups.
    """

    __table_args__ = (
        UniqueConstraint(
            "name",
            "faculty_id",
            name="group_name_faculty_id_uc",
        ),
    )

    faculty: "FacultyModel" = Relationship(back_populates="groups")
