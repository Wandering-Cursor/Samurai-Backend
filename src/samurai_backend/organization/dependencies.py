from typing import Annotated

import pydantic
from fastapi import Depends
from sqlmodel import Session

from samurai_backend.db import get_db_session_async
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.organization.department import DepartmentModel
from samurai_backend.models.organization.faculty import FacultyModel
from samurai_backend.models.organization.group import GroupModel
from samurai_backend.organization.get.department import get_department_by_id
from samurai_backend.organization.get.faculty import get_faculty_by_id
from samurai_backend.organization.get.group import get_group_by_id


def department_exists(
    db: Annotated[Session, Depends(get_db_session_async)],
    department_id: pydantic.UUID4,
) -> DepartmentModel:
    department = get_department_by_id(db, department_id)
    if department is None:
        raise SamuraiNotFoundError
    return department


def faculty_exists(
    db: Annotated[Session, Depends(get_db_session_async)],
    faculty_id: pydantic.UUID4,
) -> FacultyModel:
    faculty = get_faculty_by_id(db, faculty_id)
    if faculty is None:
        raise SamuraiNotFoundError
    return faculty


def group_exists(
    db: Annotated[Session, Depends(get_db_session_async)],
    group_id: pydantic.UUID4,
) -> GroupModel:
    group = get_group_by_id(db, group_id)
    if group is None:
        raise SamuraiNotFoundError
    return group
