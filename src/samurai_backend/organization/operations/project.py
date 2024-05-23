import pydantic
from sqlmodel import Session

from samurai_backend.account.get.account import (
    get_all_accounts_by_faculty,
    get_all_accounts_by_group,
)
from samurai_backend.admin.schemas.project import BatchCreateProject
from samurai_backend.enums.account_type import AccountType
from samurai_backend.log import events_logger
from samurai_backend.models.projects.project import ProjectModel
from samurai_backend.models.projects.task import TaskModel
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel
from samurai_backend.organization.schemas.project import ProjectAssignInput, ProjectAssignOutput


def __get_students_from_group(session: Session, group_id: pydantic.UUID4) -> list[pydantic.UUID4]:
    return [
        account.account_id
        for account in get_all_accounts_by_group(
            session,
            group_id,
            account_type=AccountType.STUDENT,
        )
    ]


def __get_overseer_from_faculty(
    session: Session, faculty_id: pydantic.UUID4
) -> list[pydantic.UUID4]:
    return [
        account.account_id
        for account in get_all_accounts_by_faculty(
            session,
            faculty_id,
            account_type=AccountType.OVERSEER,
        )
    ]


def __make_user_project_links(
    user_project_id: pydantic.UUID4,
    account_ids: list[pydantic.UUID4],
) -> list[UserProjectLinkModel]:
    return [
        UserProjectLinkModel(
            account_id=account_id,
            user_project_id=user_project_id,
        )
        for account_id in account_ids
    ]


def __assign_per_student(
    session: Session,
    student_id: pydantic.UUID4,
    project: ProjectModel,
    teacher_ids: list[pydantic.UUID4],
) -> None:
    user_project = UserProjectModel(**project.model_dump(exclude={"project_id"}), account_links=[])
    link = UserProjectLinkModel(
        account_id=student_id,
        user_project_id=user_project.project_id,
    )
    user_project.account_links.append(link)
    user_project.account_links.extend(
        __make_user_project_links(
            user_project_id=user_project.project_id,
            account_ids=teacher_ids,
        )
    )
    user_project.account_links.extend(
        __make_user_project_links(
            user_project_id=user_project.project_id,
            account_ids=__get_overseer_from_faculty(session, project.faculty_id),
        )
    )
    session.add(link)

    for task in project.tasks:
        new_task = UserTaskModel(**task.model_dump(exclude={"task_id"}))
        user_project.tasks.append(new_task)
    session.add(user_project)
    session.commit()


def _assign_per_group(
    session: Session,
    group_id: pydantic.UUID4,
    project: ProjectModel,
    teacher_ids: list[pydantic.UUID4],
) -> int:
    students = __get_students_from_group(session, group_id)
    for student in students:
        __assign_per_student(session, student, project, teacher_ids=teacher_ids)
    return len(students)


def assign_project(
    session: Session,
    assign_input: ProjectAssignInput,
    project: ProjectModel,
) -> ProjectAssignOutput:
    students_assigned = 0
    project_copy = project.model_copy()
    teacher_ids = assign_input.teachers_ids or []

    if assign_input.students_ids:
        for student_id in assign_input.students_ids:
            __assign_per_student(
                session=session,
                student_id=student_id,
                project=project_copy,
                teacher_ids=teacher_ids,
            )
            students_assigned += 1

    if assign_input.group_ids:
        for group_id in assign_input.group_ids:
            students_assigned += _assign_per_group(
                session=session,
                group_id=group_id,
                project=project_copy,
                teacher_ids=teacher_ids,
            )

    return ProjectAssignOutput(
        students_assigned=students_assigned,
    )


def create_project_from_batch(
    session: Session,
    template: BatchCreateProject,
) -> None:
    events_logger.info(
        "Creating project from batch",
        extra={"project_name": template.name},
    )

    project = ProjectModel(
        name=template.name,
        description=template.description,
        faculty_id=template.faculty_id,
    )

    session.add(project)

    for task in template.tasks:
        task_entity = TaskModel(
            name=task.name,
            description=task.description,
            priority=task.priority,
            reviewer=task.reviewer,
            due_date=task.due_date,
            project_id=project.project_id,
        )
        session.add(task_entity)

    session.commit()
    events_logger.info(
        "Project created from batch",
        extra={"project_name": template.name},
    )
