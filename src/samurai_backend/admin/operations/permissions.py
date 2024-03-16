import pydantic
from sqlmodel import Session, SQLModel

from samurai_backend.admin.get.permissions import get_permission


def add_permissions(db: Session, entity: SQLModel, permissions: list[pydantic.UUID4]) -> SQLModel:
    entity.permissions = [
        get_permission(
            db=db,
            permission_id=permission_id,
        )
        for permission_id in permissions
    ]
    return entity
