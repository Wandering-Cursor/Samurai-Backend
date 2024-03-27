import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship

from .base import BaseNamed

if TYPE_CHECKING:
    from .task import TaskModel


class BaseProject(BaseNamed):
    faculty_id: pydantic.UUID4 = Field(
        foreign_key="facultymodel.faculty_id",
    )


class CreateProject(BaseProject):
    pass


class ProjectRepresentation(BaseProject):
    project_id: pydantic.UUID4
    tasks: list["TaskModel"]


class ProjectModel(BaseProject, table=True):
    project_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    tasks: list["TaskModel"] = Relationship(back_populates="project")
