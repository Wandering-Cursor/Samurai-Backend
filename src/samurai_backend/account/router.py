from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends

from samurai_backend.account import operations as account_operations
from samurai_backend.account.get import account as account_get
from samurai_backend.account.schemas.account import account as account_schema
from samurai_backend.dependencies import account_type, database_session, database_session_type
from samurai_backend.enums import Permissions
from samurai_backend.errors import SamuraiErrorModel, SamuraiNotFoundError

from .schemas.register import (
    ConfirmEmail,
    ConfirmEmailResponse,
    RegisterAccount,
    RegisterAccountResponse,
)

account_router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={
        400: {"model": SamuraiErrorModel},
    },
)


@account_router.post(
    "/register",
    description="Register a new account.",
)
async def register_account(
    db: Annotated[database_session_type, Depends(database_session)],
    body: Annotated[RegisterAccount, Body()],
    background_tasks: BackgroundTasks,
) -> RegisterAccountResponse:
    account = account_get.get_account(
        session=db,
        search=account_schema.AccountSearchSchema(registration_code=body.registration_code),
    )

    if not account:
        raise SamuraiNotFoundError

    account_operations.register_account(
        db=db,
        account=account,
        registration_info=body,
        tasks=background_tasks,
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


@account_router.get(
    "/me",
)
async def get_me(
    user_dependency: Annotated[account_type, Permissions.blank_security()],
    db: Annotated[database_session_type, Depends(database_session)],
) -> account_schema.VerboseAccountRepresentation:
    account_entity = account_get.get_account_by_id(
        session=db,
        account_id=user_dependency.account_id,
    )

    if not account_entity:
        raise SamuraiNotFoundError

    return account_schema.VerboseAccountRepresentation.model_validate(account_entity)


@account_router.get(
    "/search",
    dependencies=[
        Permissions.blank_security(),
    ],
)
async def search_accounts(
    search: Annotated[account_schema.AccountSimpleSearchSchema, Depends()],
    session: Annotated[database_session_type, Depends(database_session)],
) -> account_schema.VerboseAccountRepresentation:
    """
    This endpoint allows anyone with authorization to look for another user,
    for search you can provide: account_id, email or username.
    Match has to be exact, otherwise, the user will not be found.
    Only one result per search is returned.
    """
    account = account_get.get_account_by_simple_search(
        session=session,
        search=search,
    )

    if not account:
        raise SamuraiNotFoundError

    return account_schema.VerboseAccountRepresentation.model_validate(account)
