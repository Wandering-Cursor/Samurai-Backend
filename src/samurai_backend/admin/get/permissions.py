from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.models.account.account_permission import AccountPermission

if TYPE_CHECKING:
    from collections.abc import Sequence

    import pydantic
    from sqlmodel import Session


def get_permissions(
    db: Session,
) -> Sequence[AccountPermission]:
    query = select(AccountPermission)
    return db.exec(query).all()


def get_permission(
    db: Session,
    permission_id: pydantic.UUID4,
) -> AccountPermission | None:
    query = select(AccountPermission).filter(
        AccountPermission.account_permission_id == permission_id
    )
    return db.exec(query).first()
