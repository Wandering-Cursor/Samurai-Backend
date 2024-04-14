import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, Form
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
        expires=(
            datetime.datetime.now(tz=datetime.UTC)
            + datetime.timedelta(minutes=security_settings.refresh_token_lifetime_minutes)
        ),
        httponly=True,
        secure=True,
        domain=security_settings.cookie_domain,
        samesite="lax",
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


refresh_body = Body(
    default=None,
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
    db: Annotated[database_session_type, Depends(database_session)],
    refresh_token: str | None = Cookie(default=None),
    refresh_body: RefreshTokenInput | None = refresh_body,
) -> JSONResponse:
    refresh_token_value = refresh_token
    if refresh_body and refresh_body.refresh_token:
        refresh_token_value = refresh_body.refresh_token

    if not refresh_token_value:
        return JSONResponse(
            content={"detail": "No refresh token provided."},
            status_code=401,
        )

    try:
        token = authenticate_by_refresh_token(
            db=db,
            refresh_token=refresh_token_value,
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


@auth_router.post(
    "/logout",
    description="Delete the Refresh token and the session.",
    responses={
        200: {
            "description": "Logged out.",
        },
    },
)
async def logout() -> JSONResponse:
    response = JSONResponse(
        content="OK",
        status_code=200,
    )
    response.delete_cookie(
        "refresh_token",
        path="/",
        domain=security_settings.cookie_domain,
        secure=True,
        httponly=True,
        samesite="lax",
    )
    return response
