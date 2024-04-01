from fastapi import APIRouter, Security

from samurai_backend.dependencies import (
    get_current_active_account,
)

projects_read = Security(
    get_current_active_account,
    scopes=["projects:read"],
)
projects_update = Security(
    get_current_active_account,
    scopes=["projects:update"],
)
projects_delete = Security(
    get_current_active_account,
    scopes=["projects:delete"],
)

user_projects_router = APIRouter(
    prefix="/projects",
    dependencies=[
        Security(
            get_current_active_account,
        )
    ],
    tags=["student", "teacher", "overseer", "projects"],
)
