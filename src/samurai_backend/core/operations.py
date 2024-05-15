import os

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlmodel import Session, SQLModel, update

from samurai_backend.core.get import generate_file_path
from samurai_backend.dependencies import (
    account_type,
)
from samurai_backend.errors import SamuraiIntegrityError, SamuraiInvalidRequestError
from samurai_backend.models.common.file_or_text import FileModel


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


def store_file(
    session: Session,
    upload: UploadFile,
    user: account_type,
) -> FileModel:
    prohibited_file_types = [
        "",
        "exe",
        "sh",
        "bat",
        "cmd",
        "msi",
        "app",
        "appimage",
        "msix",
        "msixbundle",
        "jar",
        "apk",
        "iso",
        "dmg",
        "pkg",
        "deb",
        "rpm",
    ]

    file_name = upload.filename

    try:
        file_extension = file_name.split(".")[-1].lower()
    except IndexError:
        # handled later
        file_extension = ""

    file_size = upload.size

    if file_size > 32 * 1000 * 1000:  # 32 MB
        raise SamuraiInvalidRequestError(detail_override="File size is too large.")

    if file_extension in prohibited_file_types:
        raise SamuraiInvalidRequestError(detail_override="File type is not allowed.")

    file_entity = FileModel(
        file_name=file_name,
        file_type=upload.content_type,
        file_size=file_size,
        uploaded_by_id=user.account_id,
        file_path="",
    )

    file_path = generate_file_path(file_entity)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as file:
        file.write(upload.file.read())

    file_entity.file_path = file_path

    return store_entity(session, file_entity)
