from fastapi import APIRouter, Security

from samurai_backend.dependencies import (
    get_current_active_account,
)

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[
        Security(
            get_current_active_account,
            scopes=["admin"],
        )
    ],
    tags=["admin"],
)
