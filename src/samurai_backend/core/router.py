from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from samurai_backend.core.schemas import ErrorSchema, GetToken, RefreshTokenInput, Token
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.settings import security_settings

from .dependencies import authenticate, authenticate_by_refresh_token

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


def perform_login(db: database_session_type, auth_data: GetToken) -> JSONResponse:
    try:
        token, refresh = authenticate(
            db=db,
            username=auth_data.username,
            password=auth_data.password,
            access_token_ttl_min=auth_data.access_token_ttl_min,
        )
    except ValueError:
        return JSONResponse(
            content={"detail": "Could not validate credentials"},
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
        secure=True,
    )

    return response


@auth_router.post(
    "/token",
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
    return perform_login(db, auth_data)


@auth_router.post(
    "/token/form",
    include_in_schema=False,
)
async def login_form(
    db: Annotated[database_session_type, Depends(database_session)],
    username: str = Form(),
    password: str = Form(),
    access_token_ttl_min: int = Form(None),
) -> JSONResponse:
    return perform_login(
        db,
        GetToken(
            username=username,
            password=password,
            access_token_ttl_min=access_token_ttl_min,
        ),
    )


@auth_router.post(
    "/refresh",
    description="Refresh the Access token using the Refresh token stored in a cookie.",
    responses={
        200: {
            "description": "Access token refreshed.",
            "model": Token,
        },
    },
)
async def refresh_token(
    request: Request,
    db: Annotated[database_session_type, Depends(database_session)],
    refresh_body: Annotated[RefreshTokenInput | None, Body()],
) -> JSONResponse:
    refresh_token = refresh_body.refresh_token
    if cookie_token := request.cookies.get("refresh_token"):
        refresh_token = cookie_token

    if not refresh_token:
        return JSONResponse(
            content={"detail": "No refresh token provided."},
            status_code=401,
        )

    try:
        token = authenticate_by_refresh_token(
            db=db,
            refresh_token=refresh_token,
        )
    except ValueError:
        return JSONResponse(
            content={"detail": "Could not validate credentials"},
            status_code=401,
        )

    return JSONResponse(
        content=token.model_dump(mode="json"),
        status_code=200,
    )


# TODO: Implement logout endpoint (delete refresh token and session)
# TODO: Store sessions (perhaps we don't really need this :shruh:)
