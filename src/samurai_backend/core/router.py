from fastapi import APIRouter

from samurai_backend.core.schemas import ErrorSchema

auth_router = APIRouter(
    prefix="/auth",
    responses={
        401: {
            "description": "Unauthorized, or invalid credentials.",
            "model": ErrorSchema,
        }
    },
    tags=["auth"],
)

ws_router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)
