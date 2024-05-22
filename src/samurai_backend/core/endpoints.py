import datetime
from typing import Annotated
from urllib.parse import quote

import pydantic
from fastapi import Body, Cookie, Depends, Form, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from samurai_backend.core.dependencies import authenticate, authenticate_by_refresh_token
from samurai_backend.core.get import get_file_by_id, get_file_iterator
from samurai_backend.core.operations import store_file
from samurai_backend.core.router import auth_router, common_router
from samurai_backend.core.schemas import GetToken, RefreshTokenInput, Token
from samurai_backend.core.schemas.common import FileRepresentation
from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
)
from samurai_backend.enums import Permissions
from samurai_backend.settings import security_settings


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


@common_router.get(
    "/file/{file_id}",
    dependencies=[
        Permissions.blank_security(),
    ],
)
async def get_file(
    db_session: Annotated[database_session_type, Depends(database_session)],
    file_id: pydantic.UUID4,
) -> StreamingResponse:
    """Download a file by its ID."""
    file_entity = get_file_by_id(
        session=db_session,
        file_id=file_id,
    )

    return StreamingResponse(
        content=get_file_iterator(file_entity),
        headers={
            "Content-Disposition": f'attachment; filename="{quote(file_entity.file_name)}"',
            "Content-Type": file_entity.file_type,
        },
    )


@common_router.get(
    "/file/{file_id}/info",
)
async def get_file_info(
    db_session: Annotated[database_session_type, Depends(database_session)],
    file_id: pydantic.UUID4,
) -> FileRepresentation:
    """Get information about a file by its ID."""
    return FileRepresentation.model_validate(
        get_file_by_id(
            session=db_session,
            file_id=file_id,
        )
    )


@common_router.post(
    "/file",
)
async def create_file(
    user_dependency: Annotated[account_type, Permissions.blank_security()],
    db_session: Annotated[database_session_type, Depends(database_session)],
    file: UploadFile,
) -> FileRepresentation:
    """Upload a new file."""
    return FileRepresentation.model_validate(
        store_file(
            session=db_session,
            upload=file,
            user=user_dependency,
        )
    )
