from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel

from samurai_backend.errors import SamuraiIntegrityError


def store_entity(
    db: Session,
    entity: SQLModel,
) -> SQLModel:
    try:
        db.add(entity)
        db.commit()

        return entity
    except IntegrityError as e:
        db.rollback()
        raise SamuraiIntegrityError from e
