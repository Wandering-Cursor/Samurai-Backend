import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .department import DepartmentModel
    from .group import GroupModel


class FacultyModel(SQLModel, table=True):
    """
    Describes a faculty in an educational institution.
    Faculty is a sub-unit of a department.

    Faculties have a list of associated groups.
    """

    faculty_id: pydantic.UUID4 = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    department_id: pydantic.UUID4 = Field(index=True, foreign_key="departmentmodel.department_id")

    name: str
    description: str | None = Field(default=None, nullable=True)

    department: "DepartmentModel" = Relationship(back_populates="faculties")
    groups: list["GroupModel"] = Relationship(back_populates="faculty")
