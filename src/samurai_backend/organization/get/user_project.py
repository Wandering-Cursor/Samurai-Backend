from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from sqlalchemy import case, func
from sqlmodel import select

from samurai_backend.account.schemas.account_by_account_id_mixin import AccountByAccountIdMixin
from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.enums import AccountType, TaskState
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.connection import ConnectionModel
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel
from samurai_backend.organization.schemas import user_project as user_project_schemas
from samurai_backend.organization.schemas.user_project import (
    ProjectSearchInput,
    UserProjectSearchOutput,
)
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_project_by_id(
    session: Session,
    project_id: pydantic.UUID4,
) -> UserProjectModel | None:
    return session.exec(
        select(
            UserProjectModel,
        ).where(
            UserProjectModel.project_id == project_id,
        )
    ).first()


def get_linked_project_by_id(
    session: Session,
    project_id: pydantic.UUID4,
    account_id: pydantic.UUID4,
) -> UserProjectModel | None:
    return session.exec(
        select(
            UserProjectModel,
        )
        .join(
            UserProjectLinkModel,
        )
        .where(
            UserProjectModel.project_id == project_id,
            UserProjectLinkModel.account_id == account_id,
        )
    ).first()


def get_last_linked_project(
    session: Session,
    account_id: pydantic.UUID4,
) -> UserProjectModel | None:
    return session.exec(
        select(
            UserProjectModel,
        )
        .join(
            UserProjectLinkModel,
        )
        .where(
            UserProjectLinkModel.account_id == account_id,
        )
        .order_by(
            UserProjectModel.updated_at.asc(),
        )
    ).first()


def search_projects(
    session: Session,
    search_input: ProjectSearchInput,
    related_account_id: pydantic.UUID4 | None = None,
) -> UserProjectSearchOutput:
    query = select(
        UserProjectModel,
    ).order_by(
        UserProjectModel.updated_at.asc(),
    )

    if search_input.faculty_id:
        query = query.where(
            UserProjectModel.faculty_id == search_input.faculty_id,
        )
    if search_input.name:
        query = query.where(
            UserProjectModel.name.icontains(search_input.name),
        )

    if related_account_id:
        # Perform a conditional join on the UserProjectLinkModel
        # If this breaks in the future :shrug:
        query = query.join(
            UserProjectLinkModel,
            UserProjectModel.project_id == UserProjectLinkModel.user_project_id,
        ).where(
            UserProjectLinkModel.account_id == related_account_id,
        )

    total = get_count(session, query)
    query = query.offset(search_input.offset).limit(search_input.page_size)

    rows = session.exec(query)

    return UserProjectSearchOutput(
        meta=PaginationMetaInformation(
            total=total,
            page=search_input.page,
            page_size=search_input.page_size,
        ),
        content=list(rows.all()),
    )


def _get_tasks_states(tasks: list[UserTaskModel]) -> dict[TaskState, int]:
    tasks_by_state = defaultdict(int)
    for task in tasks:
        tasks_by_state[task.state] += 1
    return tasks_by_state


def get_projects_stats_by_teacher(
    session: Session,
    faculty_id: pydantic.UUID4,
) -> user_project_schemas.ProjectsStatsByTeacher:
    result: user_project_schemas.ProjectsStatsByTeacher = []

    query = (
        select(
            AccountModel,
        )
        .where(
            AccountModel.connections.any(
                ConnectionModel.faculty_id == faculty_id,
            )
        )
        .where(
            AccountModel.account_type == AccountType.TEACHER,
        )
    )

    teachers = session.exec(query)

    for teacher in teachers:
        projects_query = select(
            UserProjectModel,
        ).where(
            UserProjectModel.account_links.any(
                UserProjectLinkModel.account_id == teacher.account_id,
            )
        )
        projects_total = get_count(session, projects_query)

        tasks = session.exec(
            select(
                UserTaskModel,
            ).where(
                UserTaskModel.project.has(
                    UserProjectModel.account_links.any(
                        UserProjectLinkModel.account_id == teacher.account_id,
                    )
                )
            )
        )

        tasks_states = _get_tasks_states(tasks)

        result.append(
            user_project_schemas.ProjectStatsByTeacher(
                account_id=teacher.account_id,
                projects=user_project_schemas.ProjectStatsEntity(total=projects_total),
                tasks=tasks_states,
                tasks_total=sum(tasks_states.values()),
            )
        )

    return result


def get_projects_stats_by_task(
    session: Session,
    faculty_id: pydantic.UUID4,
    query: user_project_schemas.ProjectsStatsByTaskInput,
) -> user_project_schemas.ProjectsStatsByTask:
    subquery = (
        select(
            UserProjectModel.project_id,
            func.sum(case((UserTaskModel.state == query.order_by_state.value, 1), else_=0)).label(
                "tasks_count"
            ),
        )
        .select_from(UserProjectModel)
        .join(UserTaskModel, UserProjectModel.project_id == UserTaskModel.project_id)
        .where(UserProjectModel.faculty_id == faculty_id)
        .group_by(UserProjectModel.project_id)
        .subquery()
    )

    projects_query = (
        select(
            UserProjectModel,
        )
        .join(subquery, UserProjectModel.project_id == subquery.c.project_id)
        .order_by(getattr(subquery.c.tasks_count, query.order_direction)())
        .group_by(UserProjectModel, subquery.c.tasks_count)
        .limit(query.limit)
    )

    projects_data = session.exec(projects_query)

    result: user_project_schemas.ProjectsStatsByTask = []

    for project in projects_data:
        students = []
        teachers = []

        for link in project.account_links:
            entity = AccountByAccountIdMixin(account_id=link.account.account_id)
            match link.account.account_type:
                case AccountType.STUDENT:
                    students.append(entity)
                case AccountType.TEACHER:
                    teachers.append(entity)
                case _:
                    continue

        result.append(
            user_project_schemas.ProjectsTasksStats(
                project_id=project.project_id,
                name=project.name,
                students=students,
                teachers=teachers,
                tasks=_get_tasks_states(project.tasks),
                tasks_total=len(project.tasks),
            )
        )

    return result
