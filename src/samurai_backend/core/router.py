from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from samurai_backend.account import operations
from samurai_backend.account.schemas.account import VerboseAccountRepresentation
from samurai_backend.core.schemas import GetToken, Token
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.settings import security_settings

from .dependencies import authenticate

auth_router = APIRouter(
    prefix="/auth",
    responses={
        401: {
            "description": "Unauthorized, or invalid credentials.",
        }
    },
)


@auth_router.post(
    "/token",
    tags=["auth"],
    description="Create a pair of Access and Refresh tokens. Latter is stored in a cookie.",
    responses={
        200: {
            "description": "Access token created.",
            "model": Token,
        },
    },
)
async def login(
    db: Annotated[database_session_type, Depends(database_session)],
    auth_data: Annotated[GetToken, Body()],
) -> JSONResponse:
    try:
        token, refresh = authenticate(
            db=db,
            username=auth_data.username,
            password=auth_data.password,
            access_token_ttl_min=auth_data.access_token_ttl_min,
        )
    except ValueError as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=401,
        )

    response = JSONResponse(
        content=token.model_dump(mode="json"),
        status_code=200,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        max_age=security_settings.refresh_token_lifetime_minutes * 60,
    )

    return response


@auth_router.post("/create")
async def create_account(
    db: Annotated[database_session_type, Depends(database_session)],
    username: str,
    password: str,
) -> VerboseAccountRepresentation:
    return operations.create_account(
        db=db,
        username=username,
        password=password,
    )
