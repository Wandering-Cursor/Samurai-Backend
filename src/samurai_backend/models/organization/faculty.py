import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, UniqueConstraint

from samurai_backend.models.base import BaseModel

if TYPE_CHECKING:
    from .department import DepartmentModel
    from .group import GroupModel


class CreateFaculty(BaseModel):
    department_id: pydantic.UUID4 = Field(index=True, foreign_key="departmentmodel.department_id")

    name: str
    description: str | None = Field(default=None, nullable=True)


class Faculty(CreateFaculty):
    faculty_id: pydantic.UUID4 = Field(default_factory=uuid.uuid4, primary_key=True, index=True)


class FacultyRepresentation(Faculty):
    groups: list = pydantic.Field(default_factory=list, exclude=True)

    @pydantic.computed_field
    @property
    def groups_count(self) -> int:
        return len(self.groups)

    @pydantic.computed_field
    @property
    def _links(self) -> dict[str, dict[str, str]]:
        return {
            "self": {"href": f"/admin/faculty/{self.faculty_id}"},
            "groups": {"href": f"/admin/group?faculty_id={self.faculty_id}"},
        }


class FacultyModel(Faculty, table=True):
    """
    Describes a faculty in an educational institution.
    Faculty is a sub-unit of a department.

    Faculties have a list of associated groups.
    """

    __table_args__ = (
        UniqueConstraint(
            "name",
            "department_id",
            name="faculty_name_department_unique_constraint",
        ),
    )

    department: "DepartmentModel" = Relationship(back_populates="faculties")
    groups: list["GroupModel"] = Relationship(back_populates="faculty")
