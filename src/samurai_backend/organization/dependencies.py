from typing import Annotated

import pydantic
from fastapi import Depends

from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.organization.department import DepartmentModel
from samurai_backend.organization.get.department import get_department_by_id


def department_exists(
    db: Annotated[database_session_type, Depends(database_session)],
    department_id: pydantic.UUID4,
) -> DepartmentModel:
    department = get_department_by_id(db, department_id)
    if department is None:
        raise SamuraiNotFoundError
    return department