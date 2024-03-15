from __future__ import annotations

import secrets
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt

from samurai_backend.account.get.account import get_account
from samurai_backend.account.schemas.account import AccountSchema, AccountSearchSchema
from samurai_backend.core.schemas import TokenData
from samurai_backend.db import get_db_session
from samurai_backend.settings import security_settings, settings

if TYPE_CHECKING:
    from sqlmodel import Session

database_session_type = AsyncGenerator["Session", None, None]
database_session = get_db_session


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "admin": "Administrator level scope",
        "overseer": "Overseer level scope",
        "teacher": "Teacher level scope",
        "student": "Student level scope",
        "account": "Any account will have this scope",
    },
)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates an access token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(tz=settings.timezone) + expires_delta
    else:
        expire = datetime.now(tz=settings.timezone) + timedelta(
            minutes=security_settings.access_token_lifetime_minutes
        )
    to_encode.update({"exp": expire})
    to_encode.update({"type": "access"})

    # Add entropy to the token to reduce the chance of a collision.
    to_encode.update({"entropy": secrets.token_urlsafe(32)})

    return jwt.encode(
        to_encode,
        security_settings.secret_key,
        algorithm=security_settings.algorithm,
    )


def create_refresh_token(data: dict) -> str:
    """
    Creates a refresh token.
    """
    to_encode = data.copy()

    expire = datetime.now(tz=settings.timezone) + timedelta(
        minutes=security_settings.refresh_token_lifetime_minutes
    )

    to_encode.update({"exp": expire})
    to_encode.update({"type": "refresh"})

    # Add entropy to the token to reduce the chance of a collision.
    to_encode.update({"entropy": secrets.token_urlsafe(32)})

    return jwt.encode(
        to_encode,
        security_settings.secret_key,
        algorithm=security_settings.algorithm,
    )


def get_current_account(
    db: Annotated[Session, Depends(database_session)],
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AccountSchema:
    """
    Returns the current account from the database.
    """
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(
            token,
            security_settings.secret_key,
            algorithms=[security_settings.algorithm],
        )
        account_id: str = payload.get("sub")
        if account_id is None:
            raise JWTError

        token_type: str = payload.get("type")
        if token_type != "access":
            raise JWTError

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(
            account_id=account_id,
            scopes=token_scopes,
        )
    except JWTError as e:
        raise credentials_exception from e

    account = get_account(
        db=db,
        search=AccountSearchSchema(
            account_id=token_data.account_id,
        ),
    )
    if account is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return account


def get_current_active_account(
    current_account: Annotated[AccountSchema, Depends(get_current_account)],
) -> dict:
    """
    Returns the current active account.
    """
    if current_account["is_active"] is False:
        raise HTTPException(status_code=400, detail="Inactive account")
    return current_account
