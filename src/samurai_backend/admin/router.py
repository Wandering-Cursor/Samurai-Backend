from fastapi import APIRouter

from samurai_backend.enums.permissions import Permissions

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[
        Permissions.ADMIN.as_security,
    ],
    tags=["admin"],
)
