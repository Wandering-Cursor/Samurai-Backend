from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import SecurityScopes
from sqlmodel import Session

from samurai_backend.db import get_db_session_async
from samurai_backend.dependencies.get_current_account import get_current_account
from samurai_backend.dependencies.get_current_active_account import get_current_active_account
from samurai_backend.models.account.account import AccountModel


def ws_get_current_active_account(
    session: Annotated[Session, Depends(get_db_session_async)],
    token: Annotated[str, Header(alias="Authorization")],
    security_scopes: SecurityScopes,
) -> AccountModel:
    """
    Returns the current active account.
    """
    token = token.replace("Bearer ", "")

    current_account = get_current_account(
        db=session,
        security_scopes=security_scopes,
        token=token,
    )
    return get_current_active_account(current_account)
