import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship

from samurai_backend.models.projects.project import (
    BaseProject,
    CreateProject,
)

if TYPE_CHECKING:
    from .task import UserTaskModel
    from .user_project_link import UserProjectLinkModel


class CreateUserProject(CreateProject):
    account_links: list[pydantic.UUID4] = []


class UserProjectModel(BaseProject, table=True):
    project_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        unique=True,
    )

    account_links: list["UserProjectLinkModel"] = Relationship(back_populates="user_project")
    tasks: list["UserTaskModel"] = Relationship(back_populates="project")
