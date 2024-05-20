import pydantic
from sqlmodel import Session

from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel


def assign_to_accounts(
    session: Session,
    project: UserProjectModel,
    account_ids: list[pydantic.UUID4],
) -> UserProjectModel:
    project.account_links = []

    for account in account_ids:
        link = UserProjectLinkModel(
            account_id=account,
            user_project_id=project.project_id,
        )
        session.add(link)
        project.account_links.append(link)

    session.add(project)
    session.commit()

    return project


def delete_project(
    session: Session,
    project: UserProjectModel,
) -> None:
    session.delete(project)

    session.commit()
