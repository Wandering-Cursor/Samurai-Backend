from __future__ import annotations

import secrets
from typing import TYPE_CHECKING

from samurai_backend.account.get import account as account_get
from samurai_backend.core.operations import store_entity
from samurai_backend.db import get_db_session_object
from samurai_backend.enums.email_code_type import EmailCodeType
from samurai_backend.log import events_logger
from samurai_backend.models import account as account_models
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.registration_code import RegistrationEmailCode
from samurai_backend.third_party.email import tasks as email_tasks

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
        email_tasks.send_registration_code_email,
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


def change_password(
    session: Session,
    account: AccountModel,
    new_password: str,
    background_tasks: BackgroundTasks,
) -> None:
    account.set_password(new_password)
    store_entity(session, account)
    events_logger.info(f"Password changed for account: {account.account_id}")

    background_tasks.add_task(
        email_tasks.send_notify_password_changed_email,
        to=account.email,
    )


def start_password_reset(
    session: Session,
    background_tasks: BackgroundTasks,
    account_search: account_schemas.AccountSimpleSearchSchema,
) -> bool:
    account = account_get.get_account_by_simple_search(
        session=session,
        search=account_search,
    )

    if not account:
        events_logger.info("Password reset: Account not found.")
        return False

    new_email_code = account_models.email_code.EmailCodeModel(
        account_id=account.account_id,
        code_type=EmailCodeType.RESET_PASSWORD,
    )
    email_code = new_email_code.set_value(None)
    new_email_code.set_expiration_date()

    store_entity(session, new_email_code)
    session.commit()

    background_tasks.add_task(
        email_tasks.send_reset_password_code_email,
        to=account.email,
        code=email_code,
    )

    events_logger.info(f"Password reset started for account: {account.account_id}")

    return True


def reset_password(
    session: Session,
    email_code: str,
    new_password: str,
    background_tasks: BackgroundTasks,
) -> bool:
    email_code_entity = account_get.get_email_code(
        session=session,
        email_code=email_code,
        code_type=EmailCodeType.RESET_PASSWORD,
    )

    if not email_code_entity:
        return False

    if email_code_entity.is_expired:
        return False

    account = account_get.get_account_by_id(
        session=session,
        account_id=email_code_entity.account_id,
    )

    if not account:
        return False

    account.set_password(new_password)
    store_entity(session, account)
    email_code_entity.is_used = True
    store_entity(session, email_code_entity)

    background_tasks.add_task(
        email_tasks.send_notify_password_changed_email,
        to=account.email,
    )

    return True
