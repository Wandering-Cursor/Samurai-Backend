from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import or_
from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.connection import ConnectionModel
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session

    from samurai_backend.account.schemas.account.account import (
        AccountSearchPaginationSchema,
        AccountSearchResultVerbose,
        AccountSearchSchema,
        AccountSimpleSearchSchema,
    )


def get_account_by_id(
    session: Session,
    account_id: pydantic.UUID4,
) -> AccountModel | None:
    from samurai_backend.account.schemas.account.account import AccountSearchSchema

    return get_account(
        session,
        AccountSearchSchema(
            account_id=account_id,
        ),
    )


def get_account(
    session: Session,
    search: AccountSearchSchema,
) -> AccountModel | None:
    """
    Returns a user from the database.
    """
    filters = []
    if search.account_id:
        filters.append(AccountModel.account_id == search.account_id)

    if search.email:
        filters.append(AccountModel.email == search.email)

    if search.username:
        filters.append(AccountModel.username == search.username)

    if search.registration_code:
        filters.append(AccountModel.registration_code == search.registration_code)

    query = select(AccountModel).filter(
        or_(
            *filters,
        ),
    )
    user = session.exec(query).first()

    if not user:
        return None

    return user


def get_accounts(db: Session, search: AccountSearchPaginationSchema) -> AccountSearchResultVerbose:
    """
    Returns a list of users from the database.
    """
    from samurai_backend.account.schemas.account.account import (
        AccountSearchResultVerbose,
        VerboseAccountRepresentation,
    )

    query = select(AccountModel).order_by(
        AccountModel.updated_at.desc(),
    )

    if search.account_id:
        query = query.filter(AccountModel.account_id == search.account_id)

    if search.email or search.username:
        arguments = []
        if search.email:
            arguments.append(AccountModel.email.icontains(search.email))
        if search.username:
            arguments.append(AccountModel.username.icontains(search.username))

        email_or_username_filter = or_(
            *arguments,
        )

        query = query.filter(email_or_username_filter)

    if search.account_type:
        query = query.filter(AccountModel.account_type == search.account_type)

    if search.registration_code:
        query = query.filter(AccountModel.registration_code == search.registration_code)

    total = get_count(db, query)
    query = query.offset(search.search_page * search.page_size).limit(search.page_size)

    query = db.exec(query)

    return AccountSearchResultVerbose(
        meta=PaginationMetaInformation(
            total=total,
            page=search.page,
            page_size=search.page_size,
        ),
        content=[
            VerboseAccountRepresentation.model_validate(row, from_attributes=True)
            for row in query.all()
        ],
    )


def get_all_accounts_by_group(db: Session, group_id: pydantic.UUID4) -> list[AccountModel]:
    query = select(ConnectionModel).filter(ConnectionModel.group_id == group_id)
    query = db.exec(query)

    accounts = []
    for row in query.all():
        if row.accounts:
            accounts += row.accounts

    return accounts


def get_account_by_simple_search(
    session: Session,
    search: AccountSimpleSearchSchema,
) -> AccountModel | None:
    query = select(AccountModel)

    if search.account_id:
        query = query.filter(AccountModel.account_id == search.account_id)

    if search.email:
        query = query.filter(AccountModel.email == search.email)

    if search.username:
        query = query.filter(AccountModel.username == search.username)

    return session.exec(query).first()
