from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import delete_entity, store_entity, update_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.models.organization.department import (
    CreateDepartment,
    DepartmentModel,
    DepartmentRepresentation,
)
from samurai_backend.organization.dependencies import department_exists
from samurai_backend.organization.get.department import get_departments_search
from samurai_backend.organization.schemas.department import (
    DepartmentSearchInput,
    DepartmentSearchOutput,
)


@admin_router.post(
    "/department",
    description="Create a new department",
)
async def create_department(
    db: Annotated[database_session_type, Depends(database_session)],
    department: Annotated[CreateDepartment, Body()],
) -> DepartmentRepresentation:
    department_obj = DepartmentModel.model_validate(department)
    return DepartmentRepresentation.model_validate(
        store_entity(
            db=db,
            entity=department_obj,
        ),
        from_attributes=True,
    )


@admin_router.put(
    "/department/{department_id}",
    description="Update a department",
)
async def update_department(
    db: Annotated[database_session_type, Depends(database_session)],
    department_id: pydantic.UUID4,
    department: Annotated[CreateDepartment, Body()],
    _: Annotated[DepartmentModel, Depends(department_exists)],
) -> DepartmentRepresentation:
    department_obj = DepartmentModel.model_validate(department)
    department_obj.department_id = department_id
    return DepartmentRepresentation.model_validate(
        update_entity(
            db=db,
            entity=department_obj,
            primary_key="department_id",
        ),
        from_attributes=True,
    )


@admin_router.delete(
    "/department/{department_id}",
    description="Delete a department",
)
async def delete_department(
    db: Annotated[database_session_type, Depends(database_session)],
    department: Annotated[DepartmentModel, Depends(department_exists)],
) -> None:
    delete_entity(
        db=db,
        entity=department,
    )


@admin_router.get(
    "/department/{department_id}",
    description="Get a department by ID",
)
async def get_department_by_id(
    department: Annotated[DepartmentModel, Depends(department_exists)],
) -> DepartmentRepresentation:
    return DepartmentRepresentation.model_validate(
        department,
        from_attributes=True,
    )


@admin_router.get(
    "/department",
    description="Get all departments",
)
async def get_all_departments(
    db: Annotated[database_session_type, Depends(database_session)],
    search_input: Annotated[DepartmentSearchInput, Depends()],
) -> DepartmentSearchOutput:
    return get_departments_search(
        db,
        search=search_input,
    )
