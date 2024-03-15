from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from samurai_backend.account.get.account import get_account
from samurai_backend.account.schemas.account import AccountSearchSchema
from samurai_backend.core.schemas import Token
from samurai_backend.dependencies import create_access_token, create_refresh_token
from samurai_backend.settings import security_settings
from samurai_backend.utils import verify_password

MAX_TOKEN_TLL = security_settings.max_access_token_ttl

if TYPE_CHECKING:
    from sqlmodel import Session


def authenticate(
    db: Session,
    username: str,
    password: str,
    access_token_ttl_min: int | None = None,
) -> tuple[Token, str]:
    """Returns an Authentication Token and a Refresh Token."""
    auth_error = ValueError("Could not authenticate user.")

    account = get_account(
        db,
        search=AccountSearchSchema(
            username=username,
        ),
    )
    if not account:
        logging.error(f"Could not find account with username: {username}")
        raise auth_error

    is_password_valid = verify_password(
        salt=account.salt,
        plain_password=password,
        hashed_password=account.hashed_password,
    )
    if not is_password_valid:
        raise auth_error

    token_data = {
        "sub": username,
        "scopes": [],
    }
    return Token(
        access_token=create_access_token(
            data=token_data,
            expires_delta=access_token_ttl_min,
        ),
        token_type="bearer",
    ), create_refresh_token(
        data=token_data,
    )
