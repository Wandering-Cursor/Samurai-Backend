from sqlalchemy.orm import Session

from . import models, schemas


def get_bases(db: Session, skip: int = 0, limit: int = 100) -> list[models.BaseModel]:
    return db.query(models.BaseModel).offset(skip).limit(limit).all()


def insert_base(db: Session, base: schemas.BaseModel) -> models.BaseModel:
    db_base = models.BaseModel(**base.model_dump())
    db.add(db_base)
    db.commit()
    db.refresh(db_base)
    return db_base
