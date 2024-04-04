import pydantic

from samurai_backend.core.schemas import (
    BasePaginatedResponse,
    PaginationSearchSchema,
)
from samurai_backend.models.user_projects.comment import CreateComment as CreateCommentModel


class CreateComment(CreateCommentModel):
    task_id: pydantic.UUID4 | None = pydantic.Field(default=None, exclude=True)
    sender_id: pydantic.UUID4 | None = pydantic.Field(default=None, exclude=True)

    created_at: None = pydantic.Field(default=None, exclude=True)
    updated_at: None = pydantic.Field(default=None, exclude=True)


class CommentRepresentation(CreateCommentModel):
    comment_id: pydantic.UUID4


class CommentSearchSchema(PaginationSearchSchema):
    page_size: int = pydantic.Field(
        default=25,
        ge=1,
    )
    task_id: pydantic.UUID4


class CommentPaginatedResponse(BasePaginatedResponse):
    content: list[CommentRepresentation]
