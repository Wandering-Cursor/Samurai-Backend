import uuid

import pydantic
from sqlalchemy.event import listen
from sqlmodel import Field, Relationship

from samurai_backend.models.base import BaseModel
from samurai_backend.utils.update_time import update_time

from .faculty import FacultyModel


class BaseDepartment(BaseModel):
    name: str = Field(unique=True, index=True)
    description: str | None = Field(default=None, nullable=True)


class CreateDepartment(BaseDepartment):
    pass


class DepartmentRepresentation(BaseDepartment):
    department_id: pydantic.UUID4
    faculties: list = pydantic.Field(default_factory=list, exclude=True)

    @pydantic.computed_field
    @property
    def faculties_count(self) -> int:
        return len(self.faculties)

    @pydantic.computed_field
    @property
    def _links(self) -> dict[str, dict[str, str]]:
        return {
            "self": {"href": f"/admin/department/{self.department_id}"},
            "faculties": {"href": f"/admin/faculty?department_id={self.department_id}"},
        }


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


listen(DepartmentModel, "before_update", update_time)
