from typing import Annotated

from fastapi import HTTPException, Security, status

from samurai_backend.dependencies.get_current_account import get_current_account
from samurai_backend.models.account.account import AccountModel


def get_current_active_account(
    current_account: Annotated[
        AccountModel,
        Security(
            get_current_account,
            scopes=[],
        ),
    ],
) -> AccountModel:
    """
    Returns the current active account.
    """
    if current_account.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
        )
    if current_account.is_email_verified is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
        )

    return current_account
