from __future__ import annotations

import secrets
from typing import TYPE_CHECKING

from samurai_backend.core.operations import store_entity
from samurai_backend.db import get_db_session_object
from samurai_backend.log import events_logger
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.registration_code import RegistrationEmailCode
from samurai_backend.third_party.email.tasks import send_registration_code_email

from .get.registration_code import get_registration_code

if TYPE_CHECKING:
    from fastapi import BackgroundTasks
    from sqlmodel import Session

    from samurai_backend.account.schemas.account import account as account_schemas
    from samurai_backend.account.schemas.register import RegisterAccount


def register_account(
    db: Session,
    account: AccountModel,
    registration_info: RegisterAccount,
    tasks: BackgroundTasks,
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
    tasks.add_task(
        send_registration_code_email,
        account.email,
        registration_code.code,
    )

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


def create_batch_accounts(
    accounts_data: account_schemas.AccountBatchCreateInput,
) -> None:
    from samurai_backend.admin.operations.connections import add_connections_for_batch
    from samurai_backend.admin.operations.permissions import set_permissions

    accounts_count = len(accounts_data.accounts)

    events_logger.info(f"Creating batch accounts: {accounts_count} entities pending.")
    session = get_db_session_object()

    for index, account_data in enumerate(accounts_data.accounts):
        account = AccountModel(
            account_type=account_data.account_type,
            first_name=account_data.first_name,
            last_name=account_data.last_name,
            middle_name=account_data.middle_name,
            is_email_verified=account_data.is_email_verified,
        )
        account.set_password(secrets.token_hex(32))
        account = store_entity(session, account)

        account = add_connections_for_batch(
            session=session,
            entity=account,
            connections=account_data.connections,
            commit=False,
        )
        account = set_permissions(
            session=session,
            entity=account,
            permissions=account_data.permissions,
        )
        events_logger.info(f"Account created: {account.account_id} ({index + 1}/{accounts_count})")

    session.commit()
