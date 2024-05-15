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

common_router = APIRouter(
    prefix="/common",
    tags=["common"],
    responses={
        401: {
            "description": "Unauthorized, or invalid credentials.",
            "model": ErrorSchema,
        }
    },
)

ws_router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)
