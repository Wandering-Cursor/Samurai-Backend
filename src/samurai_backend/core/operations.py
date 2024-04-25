from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlmodel import Session, SQLModel, update

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


def update_entity(
    db: Session,
    entity: SQLModel,
    primary_key: str,
) -> SQLModel:
    try:
        entity_class = entity.__class__
        update_query = (
            update(entity_class)
            .where(getattr(entity_class, primary_key) == getattr(entity, primary_key))
            .values(**entity.model_dump(exclude={primary_key}))
        )
        db.exec(update_query)
        db.commit()

        return entity
    except (IntegrityError, InvalidRequestError) as e:
        db.rollback()
        raise SamuraiIntegrityError from e


def delete_entity(
    session: Session,
    entity: SQLModel,
    commit: bool = True,
) -> None:
    try:
        session.delete(entity)

        if commit:
            session.commit()
    except IntegrityError as e:
        session.rollback()
        raise SamuraiIntegrityError from e
