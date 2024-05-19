from typing import Annotated

import pydantic
from fastapi import BackgroundTasks, Body, Depends

from samurai_backend.account.get import account as account_get
from samurai_backend.account.operations import create_batch_accounts
from samurai_backend.account.schemas.account import account as account_schemas
from samurai_backend.account.schemas.account.account_model_schema import AccountModelSchema
from samurai_backend.admin.operations.connections import add_connections
from samurai_backend.admin.operations.permissions import set_permissions
from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import store_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.models.account.account import AccountModel, CreateAccountModel


@admin_router.post(
    "/account/create",
    description="Create a new account.",
)
async def create_account(
    db: Annotated[database_session_type, Depends(database_session)],
    account_data: Annotated[CreateAccountModel, Body()],
) -> AccountModelSchema:
    account = AccountModel.from_create_model(account_data)

    account = store_entity(
        db=db,
        entity=account,
    )

    if account_data.permissions:
        account = set_permissions(session=db, entity=account, permissions=account_data.permissions)
        account = store_entity(db=db, entity=account)
    if account_data.connections:
        account = add_connections(session=db, entity=account, connections=account_data.connections)
        account = store_entity(db=db, entity=account)

    return AccountModelSchema.model_validate(
        account,
        from_attributes=True,
    )


@admin_router.get(
    "/account/{account_id}",
    description="Get account by ID.",
)
async def get_account(
    db: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[account_schemas.AccountSearchSchema, Depends()],
) -> AccountModelSchema:
    return AccountModelSchema.model_validate(
        account_get.get_account(db, search=search),
        from_attributes=True,
    )


@admin_router.get(
    "/account",
    description="Search for accounts.",
)
async def get_all_accounts(
    db: Annotated[database_session_type, Depends(database_session)],
    search_query: Annotated[account_schemas.AccountSearchPaginationSchema, Depends()],
) -> account_schemas.AccountSearchResultVerbose:
    return account_get.get_accounts(db, search=search_query)


@admin_router.post(
    "/account/{account_id}/permissions",
)
async def set_permissions_endpoint(
    db: Annotated[database_session_type, Depends(database_session)],
    account_id: pydantic.UUID4,
    permission_input: Annotated[account_schemas.AccountSetPermissionsInput, Body()],
) -> AccountModelSchema:
    """Update permissions for the specified account"""
    account = account_get.get_account(
        db,
        search=account_schemas.AccountSearchSchema(
            account_id=account_id,
        ),
    )

    account = set_permissions(
        session=db,
        entity=account,
        permissions=permission_input.permissions,
    )
    account = store_entity(db=db, entity=account)

    return AccountModelSchema.model_validate(
        account,
        from_attributes=True,
    )


@admin_router.post(
    "/account/{account_id}/connections",
)
async def set_connections_endpoint(
    db: Annotated[database_session_type, Depends(database_session)],
    account_id: pydantic.UUID4,
    connection_input: Annotated[account_schemas.AccountSetConnectionsInput, Body()],
) -> AccountModelSchema:
    """Update permissions for the specified account"""
    account = account_get.get_account(
        db,
        search=account_schemas.AccountSearchSchema(
            account_id=account_id,
        ),
    )

    account = add_connections(
        session=db,
        entity=account,
        connections=connection_input.connections,
    )
    account = store_entity(db=db, entity=account)

    return AccountModelSchema.model_validate(
        account,
        from_attributes=True,
    )


@admin_router.post(
    "/account/batch",
)
async def batch_create_accounts(
    accounts_data: Annotated[account_schemas.AccountBatchCreateInput, Body()],
    background_tasks: BackgroundTasks,
) -> account_schemas.AccountBatchCreateOutput:
    background_tasks.add_task(
        create_batch_accounts,
        accounts_data=accounts_data,
    )

    return account_schemas.AccountBatchCreateOutput()
