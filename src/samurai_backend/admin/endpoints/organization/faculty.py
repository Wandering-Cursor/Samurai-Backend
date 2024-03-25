from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import delete_entity, store_entity, update_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.models.organization.faculty import CreateFaculty, Faculty, FacultyModel
from samurai_backend.organization.dependencies import faculty_exists
from samurai_backend.organization.get.faculty import get_faculty_search
from samurai_backend.organization.schemas.faculty import FacultySearchInput, FacultySearchOutput


@admin_router.post("/faculty")
async def create_faculty(
    db: Annotated[database_session_type, Depends(database_session)],
    faculty_data: Annotated[CreateFaculty, Body()],
) -> Faculty:
    faculty_instance = FacultyModel.model_validate(faculty_data, from_attributes=True)

    store_entity(
        db=db,
        entity=faculty_instance,
    )

    return Faculty.model_validate(faculty_instance, from_attributes=True)


@admin_router.get("/faculty")
async def get_faculties(
    db: Annotated[database_session_type, Depends(database_session)],
    search_data: Annotated[FacultySearchInput, Depends()],
) -> FacultySearchOutput:
    return get_faculty_search(
        session=db,
        search=search_data,
    )


@admin_router.get("/faculty/{faculty_id}")
async def get_faculty(
    faculty: Annotated[FacultyModel, Depends(faculty_exists)],
) -> Faculty:
    return Faculty.model_validate(faculty, from_attributes=True)


@admin_router.put("/faculty/{faculty_id}")
async def update_faculty(
    db: Annotated[database_session_type, Depends(database_session)],
    faculty_id: pydantic.UUID4,
    faculty_data: Annotated[CreateFaculty, Body()],
) -> Faculty:
    data = faculty_data.model_dump()
    data["faculty_id"] = faculty_id

    new_faculty = update_entity(
        db=db,
        entity=FacultyModel.model_validate(data),
        primary_key="faculty_id",
    )

    return Faculty.model_validate(new_faculty, from_attributes=True)


@admin_router.delete(
    "/faculty/{faculty_id}",
    status_code=204,
)
async def delete_faculty(
    db: Annotated[database_session_type, Depends(database_session)],
    faculty: Annotated[FacultyModel, Depends(faculty_exists)],
) -> None:
    delete_entity(db=db, entity=faculty)
