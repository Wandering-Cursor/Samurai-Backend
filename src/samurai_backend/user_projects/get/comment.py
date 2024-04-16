from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.user_projects.comment import CommentModel
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel
from samurai_backend.user_projects.schemas.comment import (
    CommentPaginatedResponse,
    CommentSearchSchema,
)
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_comment_by_id(
    session: Session,
    comment_id: pydantic.UUID4,
    account_id: pydantic.UUID4,
) -> CommentModel | None:
    value = session.exec(
        select(
            CommentModel,
        ).where(
            CommentModel.comment_id == comment_id,
            CommentModel.task.has(
                UserTaskModel.project.has(
                    UserProjectModel.account_links.any(
                        UserProjectLinkModel.account_id == account_id,
                    ),
                ),
            ),
        )
    ).first()

    if not value:
        return None

    return value


def search_comments(
    session: Session,
    search_input: CommentSearchSchema,
    account_id: pydantic.UUID4,
) -> CommentPaginatedResponse:
    query = select(
        CommentModel,
    ).order_by(
        CommentModel.updated_at.desc(),
    )

    query = query.where(
        CommentModel.task.has(
            UserTaskModel.project.has(
                UserProjectModel.account_links.any(
                    UserProjectLinkModel.account_id == account_id,
                ),
            ),
        ),
    )

    total_count = get_count(session, query)

    query = query.offset(search_input.offset)
    query = query.limit(search_input.page_size)

    comments = session.exec(query).all()

    return CommentPaginatedResponse(
        meta=PaginationMetaInformation(
            total=total_count,
            page=search_input.page,
            page_size=search_input.page_size,
        ),
        content=comments,
    )
