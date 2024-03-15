from __future__ import annotations

from typing import TYPE_CHECKING

from samurai_backend.models.account.account import AccountModel

if TYPE_CHECKING:
    from sqlmodel import Session


def create_account(
    db: Session,
    username: str,
    password: str,
) -> AccountModel:
    account = AccountModel(
        username=username,
        first_name="Test",
        last_name="User",
        is_email_verified=True,
    )

    account.set_password(password)

    db.add(account)
    db.commit()

    return account
