import uuid

import pydantic
from sqlmodel import Field, Relationship, SQLModel

from .faculty import Faculty, FacultyModel


class BaseDepartment(SQLModel):
    name: str = Field(unique=True, index=True)
    description: str | None = Field(default=None, nullable=True)


class CreateDepartment(BaseDepartment):
    pass


class DepartmentRepresentation(BaseDepartment):
    department_id: pydantic.UUID4
    faculties: list[Faculty]


class DepartmentModel(BaseDepartment, table=True):
    """
    Describes a department in an educational institution.
    Highest level of organization in an educational institution.

    Departments have a list of associated faculties.
    """

    department_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    faculties: list[FacultyModel] = Relationship(back_populates="department")
