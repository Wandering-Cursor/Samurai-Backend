import pydantic
from sqlmodel import Session

from samurai_backend.enums import Permissions, TaskState
from samurai_backend.errors import SamuraiInvalidRequestError, SamuraiNotFoundError
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.organization.get.user_task import get_task_by_id
from samurai_backend.organization.schemas.user_task import UserTaskStatusUpdateInput


def _check_status_update_valid(
    task: UserTaskModel,
    update: UserTaskStatusUpdateInput,
) -> None:
    if task.state == update.state:
        return

    valid_change = {
        TaskState.OPEN: [TaskState.IN_PROGRESS],
        TaskState.RESUBMIT: [TaskState.OPEN, TaskState.IN_PROGRESS],
        TaskState.IN_PROGRESS: [TaskState.OPEN, TaskState.IN_REVIEW],
        TaskState.IN_REVIEW: [TaskState.RESUBMIT, TaskState.DONE],
        TaskState.DONE: [],
    }

    if update.state not in valid_change[task.state]:
        raise SamuraiInvalidRequestError(
            detail_override="Invalid state transition",
        )


def __is_editor(updater: AccountModel) -> bool:
    return any(
        updater.has_permission(permission)
        for permission in [
            Permissions.TASKS_EDITOR,
            Permissions.TASKS_EDITOR_UPDATE,
        ]
    )


def _validate_review_update(
    task: UserTaskModel,
    updater: AccountModel,
) -> None:
    if task.state == TaskState.IN_REVIEW and not __is_editor(updater):
        raise SamuraiInvalidRequestError(
            detail_override="Only editors can update tasks in review",
        )


def update_task_state(
    session: Session,
    task_id: pydantic.UUID4,
    update: UserTaskStatusUpdateInput,
    updater: AccountModel,
) -> UserTaskModel:
    task = get_task_by_id(
        session=session,
        task_id=task_id,
        account_id=updater.account_id,
    )

    if task is None:
        raise SamuraiNotFoundError

    _check_status_update_valid(
        task=task,
        update=update,
    )
    _validate_review_update(
        task=task,
        updater=updater,
    )

    task.state = update.state
    session.add(task)
    session.commit()

    return task
