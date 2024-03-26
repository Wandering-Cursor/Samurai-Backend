from typing import Annotated

from fastapi import APIRouter, Body, Depends

from samurai_backend.account import operations as account_operations
from samurai_backend.account.get import account as account_get
from samurai_backend.account.schemas.account import AccountSearchSchema
from samurai_backend.dependencies import database_session, database_session_type

from .schemas.register import (
    ConfirmEmail,
    ConfirmEmailResponse,
    RegisterAccount,
    RegisterAccountResponse,
)

account_router = APIRouter(
    prefix="/account",
    tags=["account"],
)


@account_router.post(
    "/register",
    description="Register a new account.",
)
async def register_account(
    db: Annotated[database_session_type, Depends(database_session)],
    body: Annotated[RegisterAccount, Body()],
) -> RegisterAccountResponse:
    account = account_get.get_account(
        db=db, search=AccountSearchSchema(registration_code=body.registration_code)
    )

    if not account:
        raise ValueError("Invalid registration code.")

    account_operations.register_account(
        db=db,
        account=account,
        registration_info=body,
    )

    return RegisterAccountResponse()


@account_router.post(
    "/confirm-email",
    description="Confirm the registration email.",
)
async def confirm_email(
    db: Annotated[database_session_type, Depends(database_session)],
    body: Annotated[ConfirmEmail, Body()],
) -> ConfirmEmailResponse:
    account_operations.confirm_email(
        db=db,
        email_code=body.email_code,
    )

    return ConfirmEmailResponse()
