from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.account.get import account
from samurai_backend.account.operations import store_account
from samurai_backend.account.schemas.account import (
    AccountSearchPaginationSchema,
    AccountSearchResultVerbose,
)
from samurai_backend.admin.operations.connections import add_connections
from samurai_backend.admin.operations.permissions import add_permissions
from samurai_backend.admin.router import admin_router
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.models.account.account import AccountModel, CreateAccountModel
from samurai_backend.models.account.account_model_schema import AccountModelSchema


@admin_router.post(
    "/account/create",
    description="Create a new account.",
)
async def create_account(
    db: Annotated[database_session_type, Depends(database_session)],
    account_data: Annotated[CreateAccountModel, Body()],
) -> AccountModelSchema:
    account = AccountModel.from_create_model(account_data)

    account = store_account(
        db=db,
        account=account,
    )

    if account_data.permissions:
        account = add_permissions(db=db, entity=account, permissions=account_data.permissions)
        account = store_account(db=db, account=account)
    if account_data.connections:
        account = add_connections(db=db, entity=account, connections=account_data.connections)
        account = store_account(db=db, account=account)

    return account


@admin_router.get(
    "/account/{account_id}",
    description="Get account by ID.",
)
async def get_account(
    db: Annotated[database_session_type, Depends(database_session)],
    account_id: pydantic.UUID4,
) -> AccountModelSchema:
    return account.get_account(db, search=AccountModel(account_id=account_id))


@admin_router.get(
    "/account",
    description="Search for accounts.",
)
async def get_all_accounts(
    db: Annotated[database_session_type, Depends(database_session)],
    search_query: Annotated[AccountModel, Depends(AccountSearchPaginationSchema)],
) -> AccountSearchResultVerbose:
    return account.get_accounts(db, search=search_query)
