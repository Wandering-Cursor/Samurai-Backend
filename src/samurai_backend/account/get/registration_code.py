from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import or_
from sqlmodel import select

from samurai_backend.models.account.registration_code import RegistrationEmailCode

if TYPE_CHECKING:
    from sqlmodel import Session


def get_registration_code(db: Session, code_value: str) -> RegistrationEmailCode | None:
    query = select(RegistrationEmailCode).filter(
        or_(
            RegistrationEmailCode.code == code_value,
        ),
        RegistrationEmailCode.is_used == False,  # noqa: E712
    )
    return db.exec(query).first()
