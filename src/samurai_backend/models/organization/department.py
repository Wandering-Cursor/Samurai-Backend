import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .faculty import FacultyModel


class DepartmentModel(SQLModel, table=True):
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

    name: str = Field(unique=True, index=True)
    description: str | None = Field(default=None, nullable=True)

    faculties: list["FacultyModel"] = Relationship(back_populates="department")
