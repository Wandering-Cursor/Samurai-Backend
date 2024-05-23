import pydantic

from samurai_backend.account.schemas.account_details_mixin import AccountDetailsMixin
from samurai_backend.models.user_projects.comment import CreateComment as CreateCommentModel
from samurai_backend.schemas import (
    BasePaginatedResponse,
    PaginationSearchSchema,
)


class CreateComment(CreateCommentModel):
    task_id: pydantic.UUID4 | None = pydantic.Field(default=None, exclude=True)
    sender_id: pydantic.UUID4 | None = pydantic.Field(default=None, exclude=True)

    created_at: None = pydantic.Field(default=None, exclude=True)
    updated_at: None = pydantic.Field(default=None, exclude=True)


class CommentRepresentation(CreateCommentModel, AccountDetailsMixin):
    comment_id: pydantic.UUID4

    @property
    def _account_id(self: "CommentRepresentation") -> pydantic.UUID4:
        return self.sender_id


class CommentSearchSchema(PaginationSearchSchema):
    page_size: int = pydantic.Field(
        default=25,
        ge=1,
    )
    task_id: pydantic.UUID4


class CommentPaginatedResponse(BasePaginatedResponse):
    content: list[CommentRepresentation]
