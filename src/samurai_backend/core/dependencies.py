from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from samurai_backend.account.get.account import get_account
from samurai_backend.dependencies.create_access_token import create_access_token
from samurai_backend.dependencies.create_refresh_token import create_refresh_token
from samurai_backend.dependencies.decode_refresh_token import (
    decode_refresh_token,
)
from samurai_backend.schemas import Token, TokenData
from samurai_backend.settings import security_settings
from samurai_backend.utils.verify_password import verify_password

MAX_TOKEN_TLL = security_settings.max_access_token_ttl

if TYPE_CHECKING:
    from sqlmodel import Session

    from samurai_backend.models.account.account import AccountModel


def check_password(
    account: AccountModel,
    password: str,
) -> bool:
    return verify_password(
        salt=account.salt,
        plain_password=password,
        hashed_password=account.hashed_password,
    )


def authenticate(
    db: Session,
    username: str,
    password: str,
    access_token_ttl_min: int | None = None,
) -> tuple[Token, str]:
    """Returns an Authentication Token and a Refresh Token."""
    from samurai_backend.account.schemas.account.account import AccountSearchSchema

    auth_error = ValueError("Could not authenticate user.")

    account = get_account(
        db,
        search=AccountSearchSchema(
            username=username,
            email=username
            if "@" in username
            else None,  # Check if username is an email not to raise an error
        ),
    )
    if not account:
        logging.error(f"Could not find account with username: {username}")
        raise auth_error

    is_password_valid = check_password(account, password)
    if not is_password_valid:
        raise auth_error

    access_token_ttl = timedelta(minutes=access_token_ttl_min) if access_token_ttl_min else None

    token_data = TokenData(
        sub=account.account_id,
        scopes=[permission.name for permission in account.permissions],
    )
    return Token(
        access_token=create_access_token(
            data=token_data,
            expires_delta=access_token_ttl,
        ),
    ), create_refresh_token(
        data=token_data,
    )


def authenticate_by_refresh_token(
    db: Session,
    refresh_token: str,
) -> Token:
    """Returns a new Authentication Token."""
    from samurai_backend.account.schemas.account.account import AccountSearchSchema

    token_data = decode_refresh_token(
        token=refresh_token,
    )
    account = get_account(
        db,
        search=AccountSearchSchema(
            account_id=token_data.sub,
        ),
    )
    if not account:
        raise ValueError("Could not authenticate user.")

    token_data = TokenData(
        sub=account.account_id,
        scopes=[permission.name for permission in account.permissions],
    )
    return Token(
        access_token=create_access_token(
            data=token_data,
        ),
    )
