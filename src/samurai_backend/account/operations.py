from __future__ import annotations

from typing import TYPE_CHECKING

from samurai_backend.core.operations import store_entity
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.registration_code import RegistrationEmailCode

from .get.registration_code import get_registration_code

if TYPE_CHECKING:
    from sqlmodel import Session

    from .schemas.register import RegisterAccount


def register_account(
    db: Session,
    account: AccountModel,
    registration_info: RegisterAccount,
) -> AccountModel:
    if account.registration_email_code is not None:
        return account

    account.email = registration_info.email
    if registration_info.username:
        account.username = registration_info.username
    account.set_password(registration_info.password)

    account = AccountModel.model_validate(
        store_entity(db, account),
        from_attributes=True,
    )

    registration_code = RegistrationEmailCode(
        account_id=account.account_id,
    )
    store_entity(db, registration_code)

    return account


def confirm_email(
    db: Session,
    email_code: str,
) -> bool:
    """
    Confirm the email of the account.
    If the email code is valid, the account's email will be verified.
    Returns True if the email code is valid, False otherwise.
    """
    registration_code = get_registration_code(
        db=db,
        code_value=email_code,
    )

    if not registration_code:
        return False

    account = registration_code.account
    account.is_email_verified = True
    store_entity(db, account)
    registration_code.is_used = True
    store_entity(db, registration_code)

    return True
