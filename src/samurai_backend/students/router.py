from fastapi import APIRouter, Security

from samurai_backend.dependencies import (
    get_current_active_account,
)

student_router = APIRouter(
    prefix="/student",
    dependencies=[
        Security(
            get_current_active_account,
            scopes=["student"],
        )
    ],
    tags=["student"],
)
