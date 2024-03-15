from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import or_

from samurai_backend.account.schemas.account import AccountSchema, AccountSearchSchema
from samurai_backend.models.account.account import AccountModel

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_account(db: Session, search: AccountSearchSchema) -> AccountSchema | None:
    """
    Returns a user from the database.
    """
    user = (
        db.query(AccountModel)
        .filter(
            or_(
                AccountModel.account_id == search.account_id,
                AccountModel.email == search.email,
                AccountModel.username == search.username,
            ),
        )
        .first()
    )

    if not user:
        return None

    return AccountSchema.model_validate(user)
