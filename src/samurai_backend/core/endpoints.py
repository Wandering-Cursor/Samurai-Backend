import datetime
from typing import Annotated
from urllib.parse import quote

import pydantic
from fastapi import BackgroundTasks, Body, Cookie, Depends, Form, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from sqlmodel import Session

from samurai_backend.account import operations as account_operations
from samurai_backend.account.schemas.account.account import AccountSimpleSearchSchema
from samurai_backend.core.dependencies import (
    authenticate,
    authenticate_by_refresh_token,
    check_password,
)
from samurai_backend.core.get import get_file_by_id, get_file_iterator
from samurai_backend.core.operations import store_file
from samurai_backend.core.router import auth_router, common_router
from samurai_backend.db import get_db_session_async
from samurai_backend.enums.permissions import Permissions
from samurai_backend.errors import SamuraiInvalidRequestError, SamuraiNotFoundError
from samurai_backend.models.account.account import AccountModel
from samurai_backend.schemas import GetToken, RefreshTokenInput, Token
from samurai_backend.schemas import password as password_schemas
from samurai_backend.schemas.common import FileRepresentation
from samurai_backend.settings import security_settings


def perform_login(db: Session, auth_data: GetToken) -> JSONResponse:
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
    db: Annotated[Session, Depends(get_db_session_async)],
    auth_data: Annotated[GetToken, Body()],
) -> JSONResponse:
    return perform_login(db, auth_data)


@auth_router.post(
    "/token/form",
    include_in_schema=False,
)
async def login_form(
    db: Annotated[Session, Depends(get_db_session_async)],
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
    db: Annotated[Session, Depends(get_db_session_async)],
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


@auth_router.post("/reset-password")
async def reset_password(
    body: Annotated[password_schemas.ResetPasswordInputScheme, Body()],
    session: Annotated[Session, Depends(get_db_session_async)],
    background_tasks: BackgroundTasks,
) -> password_schemas.ResetPasswordResponseScheme:
    """Reset password. Requires entering the email address."""
    account_operations.start_password_reset(
        session=session,
        background_tasks=background_tasks,
        account_search=AccountSimpleSearchSchema(
            email=body.email,
            username=body.username,
        ),
    )

    return password_schemas.ResetPasswordResponseScheme()


@auth_router.post("/reset-password/confirm")
async def reset_password_confirm(
    body: Annotated[password_schemas.ResetPasswordConfirmInputScheme, Body()],
    session: Annotated[Session, Depends(get_db_session_async)],
    background_tasks: BackgroundTasks,
) -> password_schemas.ResetPasswordResponseScheme:
    """Confirm the password reset. Requires entering the code sent to the email."""
    is_password_reset = account_operations.reset_password(
        session=session,
        email_code=body.code,
        new_password=body.new_password,
        background_tasks=background_tasks,
    )

    if not is_password_reset:
        raise SamuraiNotFoundError("Confirmation code is invalid or expired")

    return password_schemas.ResetPasswordResponseScheme()


@auth_router.post(
    "/change-password",
)
async def change_password(
    account: Annotated[AccountModel, Permissions.blank_security()],
    session: Annotated[Session, Depends(get_db_session_async)],
    body: Annotated[password_schemas.ChangePasswordInputScheme, Body()],
    background_tasks: BackgroundTasks,
) -> password_schemas.ChangePasswordResponseScheme:
    """Change password while being authorized. Requires entering the old password, and a new one."""
    is_password_valid = check_password(
        account=account,
        password=body.old_password,
    )

    if not is_password_valid:
        raise SamuraiInvalidRequestError("Incorrect password")

    account_operations.change_password(
        session=session,
        account=account,
        new_password=body.new_password,
        background_tasks=background_tasks,
    )

    return password_schemas.ChangePasswordResponseScheme()


@common_router.get(
    "/file/{file_id}",
    dependencies=[
        Permissions.blank_security(),
    ],
)
async def get_file(
    db_session: Annotated[Session, Depends(get_db_session_async)],
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
    db_session: Annotated[Session, Depends(get_db_session_async)],
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
    user_dependency: Annotated[AccountModel, Permissions.blank_security()],
    db_session: Annotated[Session, Depends(get_db_session_async)],
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
