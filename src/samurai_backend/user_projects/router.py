from fastapi import APIRouter, Security

from samurai_backend.dependencies import (
    get_current_active_account,
)
from samurai_backend.enums import Permissions

projects_read = Security(
    get_current_active_account,
    scopes=[Permissions.PROJECTS_READ],
)
projects_update = Security(
    get_current_active_account,
    scopes=[Permissions.PROJECTS_UPDATE],
)
projects_delete = Security(
    get_current_active_account,
    scopes=[Permissions.PROJECTS_DELETE],
)

tasks_read = Security(
    get_current_active_account,
    scopes=[Permissions.TASKS_READ],
)
tasks_update = Security(
    get_current_active_account,
    scopes=[Permissions.TASKS_UPDATE],
)

tasks_editor_update = Security(
    get_current_active_account,
    scopes=[Permissions.TASKS_EDITOR_UPDATE],
)
tasks_editor_delete = Security(
    get_current_active_account,
    scopes=[Permissions.TASKS_EDITOR_DELETE],
)
tasks_editor_create = Security(
    get_current_active_account,
    scopes=[Permissions.TASKS_EDITOR_CREATE],
)

user_projects_router = APIRouter(
    prefix="/projects",
    dependencies=[
        Security(
            get_current_active_account,
        )
    ],
    tags=["teacher", "overseer", "projects"],
)
