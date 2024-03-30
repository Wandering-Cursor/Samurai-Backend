from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import or_
from sqlmodel import select

from samurai_backend.account.schemas.account import (
    AccountSearchResultVerbose,
    VerboseAccountRepresentation,
)
from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.connection import ConnectionModel
from samurai_backend.utils import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session

    from samurai_backend.account.schemas.account import (
        AccountSearchPaginationSchema,
        AccountSearchSchema,
    )


def get_account(db: Session, search: AccountSearchSchema) -> AccountModel | None:
    """
    Returns a user from the database.
    """
    query = select(AccountModel).filter(
        or_(
            AccountModel.account_id == search.account_id,
            AccountModel.email == search.email,
            AccountModel.username == search.username,
            AccountModel.registration_code == search.registration_code,
        ),
    )
    user = db.exec(query).first()

    if not user:
        return None

    return user


def get_accounts(db: Session, search: AccountSearchPaginationSchema) -> AccountSearchResultVerbose:
    """
    Returns a list of users from the database.
    """
    query = select(AccountModel)

    if search.account_id:
        query = query.filter(AccountModel.account_id == search.account_id)

    if search.email:
        query = query.filter(AccountModel.email == search.email)

    if search.username:
        query = query.filter(AccountModel.username == search.username)

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

    query = select(AccountModel).filter(
        AccountModel.account_id.in_(row.account.account_id for row in query.all())
    )

    query = db.exec(query)

    return query.all()
