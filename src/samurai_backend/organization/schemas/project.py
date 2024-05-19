import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.models.projects.project import ShortProjectRepresentation


class ProjectSearchInput(PaginationSearchSchema):
    faculty_id: pydantic.UUID4 | None = None
    name: str | None = None


class ProjectSearchOutput(BasePaginatedResponse):
    content: list[ShortProjectRepresentation]


class ProjectAssignBody(pydantic.BaseModel):
    students_ids: list[pydantic.UUID4] | None = None
    teachers_ids: list[pydantic.UUID4] | None = None
    group_ids: list[pydantic.UUID4] | None = None

    @pydantic.model_validator(mode="after")
    def ensure_one_option(self: "ProjectAssignInput") -> "ProjectAssignInput":
        if not self.students_ids and not self.group_ids:
            raise ValueError("Either students_ids or group_ids should be provided")

        return self


class ProjectAssignInput(ProjectAssignBody):
    project_id: pydantic.UUID4


class ProjectAssignOutput(pydantic.BaseModel):
    students_assigned: int
