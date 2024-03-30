import pydantic
from sqlmodel import Session

from samurai_backend.account.get.account import get_all_accounts_by_group
from samurai_backend.models.projects.project import ProjectModel
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel
from samurai_backend.organization.schemas.project import ProjectAssignInput, ProjectAssignOutput


def __get_students_from_group(session: Session, group_id: pydantic.UUID4) -> list[pydantic.UUID4]:
    return [account.account_id for account in get_all_accounts_by_group(session, group_id)]


def __assign_per_student(
    session: Session, student_id: pydantic.UUID4, project: ProjectModel
) -> None:
    user_project = UserProjectModel(**project.model_dump(), account_links=[])
    link = UserProjectLinkModel(
        account_id=student_id,
        user_project_id=user_project.project_id,
    )
    session.add(user_project)
    session.commit()
    user_project.account_links.append(link)
    session.add(link)
    session.add(user_project)
    session.commit()

    for task in project.tasks:
        user_project.tasks.append(UserTaskModel.model_validate(task, from_attributes=True))
    session.add(user_project)
    session.commit()


def _assign_per_group(session: Session, group_id: pydantic.UUID4, project: ProjectModel) -> int:
    students = __get_students_from_group(session, group_id)
    for student in students:
        __assign_per_student(session, student, project)
    return len(students)


def assign_project(
    session: Session,
    assign_input: ProjectAssignInput,
    project: ProjectModel,
) -> ProjectAssignOutput:
    students_assigned = 0

    if assign_input.students_ids:
        for student_id in assign_input.students_ids:
            __assign_per_student(
                session=session,
                student_id=student_id,
                project=project,
            )
            students_assigned += 1

    if assign_input.group_ids:
        for group_id in assign_input.group_ids:
            students_assigned += _assign_per_group(
                session=session,
                group_id=group_id,
                project=project,
            )

    return ProjectAssignOutput(
        students_assigned=students_assigned,
    )
