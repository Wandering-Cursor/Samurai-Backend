from typing import TypeVar

import pydantic
from sqlmodel import Session

from samurai_backend.admin.get.permissions import get_permission

T = TypeVar("T")


def set_permissions(session: Session, entity: T, permissions: list[pydantic.UUID4]) -> T:
    entity.permissions = [
        get_permission(
            db=session,
            permission_id=permission_id,
        )
        for permission_id in permissions
    ]
    return entity
