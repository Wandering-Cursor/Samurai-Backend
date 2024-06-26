from typing import Annotated

import pydantic
from fastapi import Body, Depends
from sqlmodel import Session

from samurai_backend.db import get_db_session_async
from samurai_backend.dependencies.get_current_active_account import get_current_active_account
from samurai_backend.enums.permissions import Permissions
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.account.account import AccountModel
from samurai_backend.user_projects.get import comment as comment_get
from samurai_backend.user_projects.operations import comment as comment_operations
from samurai_backend.user_projects.router import user_projects_router
from samurai_backend.user_projects.schemas import comment as comment_schemas


@user_projects_router.post(
    "/tasks/{task_id}/comment",
    dependencies=[
        Permissions.COMMENTS_CREATE.as_security,
    ],
    tags=["student"],
)
async def create_comment(
    task_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
    comment: Annotated[comment_schemas.CreateComment, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> comment_schemas.CommentRepresentation:
    comment.task_id = task_id
    comment.sender_id = current_user.account_id

    return comment_schemas.CommentRepresentation.model_validate(
        comment_operations.create_comment(
            session=session,
            comment=comment,
        ),
        from_attributes=True,
    )


@user_projects_router.get(
    "/tasks/{task_id}/comments",
    dependencies=[
        Permissions.COMMENTS_READ.as_security,
    ],
    tags=["student"],
)
async def get_comments(
    session: Annotated[Session, Depends(get_db_session_async)],
    search: Annotated[comment_schemas.CommentSearchSchema, Depends()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
    task_id: pydantic.UUID4,
) -> comment_schemas.CommentPaginatedResponse:
    search.task_id = task_id

    return comment_get.search_comments(
        session=session,
        search_input=search,
        account_id=current_user.account_id,
    )


@user_projects_router.get(
    "/comments/{comment_id}",
    dependencies=[
        Permissions.COMMENTS_READ.as_security,
    ],
    tags=["student"],
)
async def get_comment(
    comment_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> comment_schemas.CommentRepresentation:
    comment = comment_get.get_comment_by_id(
        session=session,
        comment_id=comment_id,
        account_id=current_user.account_id,
    )
    if not comment:
        raise SamuraiNotFoundError

    return comment_schemas.CommentRepresentation.model_validate(
        comment,
        from_attributes=True,
    )


@user_projects_router.put(
    "/comments/{comment_id}",
    dependencies=[
        Permissions.COMMENTS_UPDATE.as_security,
    ],
    tags=["student"],
)
async def update_comment(
    comment_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
    comment: Annotated[comment_schemas.CreateComment, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> comment_schemas.CommentRepresentation:
    comment = comment_operations.update_comment(
        session=session,
        comment_id=comment_id,
        comment=comment,
        account_id=current_user.account_id,
    )
    if not comment:
        raise SamuraiNotFoundError

    return comment_schemas.CommentRepresentation.model_validate(
        comment,
        from_attributes=True,
    )


@user_projects_router.delete(
    "/comments/{comment_id}",
    dependencies=[
        Permissions.COMMENTS_DELETE.as_security,
    ],
    tags=["student"],
    status_code=204,
)
async def delete_comment(
    comment_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> None:
    comment = comment_operations.delete_comment(
        session=session,
        comment_id=comment_id,
        account_id=current_user.account_id,
    )
    if not comment:
        raise SamuraiNotFoundError
