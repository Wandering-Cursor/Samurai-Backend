import pydantic
from sqlmodel import Session

from samurai_backend.core.operations import update_entity
from samurai_backend.errors import SamuraiForbiddenError, SamuraiNotFoundError
from samurai_backend.models.user_projects import comment as comment_models
from samurai_backend.organization.get.user_task import get_task_by_id
from samurai_backend.user_projects.get import comment as comment_get
from samurai_backend.user_projects.schemas import comment as comment_schemas


def create_comment(
    session: Session,
    comment: comment_schemas.CreateComment,
) -> comment_models.CommentModel:
    comment_dump = comment.model_dump()

    task = get_task_by_id(
        session=session,
        task_id=comment.task_id,
        account_id=comment.sender_id,
    )
    if not task:
        raise SamuraiNotFoundError("Task not found")

    entity = comment_models.CommentModel(
        **comment_dump,
        task_id=comment.task_id,
        sender_id=comment.sender_id,
    )

    session.add(entity)
    session.commit()

    return entity


def update_comment(
    session: Session,
    comment_id: pydantic.UUID4,
    comment: comment_schemas.CreateComment,
    account_id: pydantic.UUID4,
) -> comment_models.CommentModel:
    comment_dump = comment.model_dump()

    entity = comment_get.get_comment_by_id(
        session=session,
        comment_id=comment_id,
        account_id=account_id,
    )
    if not entity:
        raise SamuraiNotFoundError("Comment not found")

    if entity.sender_id != account_id:
        raise SamuraiForbiddenError("Cannot update comment of another user")

    new_comment = comment_models.CommentModel(
        **comment_dump,
        task_id=entity.task_id,
        sender_id=entity.sender_id,
        comment_id=entity.comment_id,
        created_at=entity.created_at,
    )

    update_entity(
        session=session,
        entity=new_comment,
        primary_key="comment_id",
    )

    return new_comment


def delete_comment(
    session: Session,
    comment_id: pydantic.UUID4,
    account_id: pydantic.UUID4,
) -> comment_models.CommentModel:
    entity = comment_get.get_comment_by_id(
        session=session,
        comment_id=comment_id,
        account_id=account_id,
    )
    if not entity:
        raise SamuraiNotFoundError("Comment not found")

    if entity.sender_id != account_id:
        raise SamuraiForbiddenError("Cannot delete comment of another user")

    session.delete(entity)
    session.commit()

    return entity
