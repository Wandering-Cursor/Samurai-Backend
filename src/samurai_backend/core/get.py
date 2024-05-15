import pydantic
from sqlmodel import Session, select

from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.common.file_or_text import FileModel


def generate_file_path(
    file_model: FileModel,
) -> str:
    return f"./files/{file_model.uploaded_by_id}/{file_model.file_id}-{hash(file_model.file_name)}"


def get_file_by_id(
    session: Session,
    file_id: pydantic.UUID4,
) -> FileModel:
    file = session.exec(select(FileModel).where(FileModel.file_id == file_id)).first()

    if not file:
        raise SamuraiNotFoundError(f"File with id {file_id} not found.")

    return file


def get_file_data_from_entity(
    file: FileModel,
) -> bytes:
    with open(file.file_path, "rb") as f:
        return f.read()


def get_file_iterator(  # noqa: ANN201
    file: FileModel,
):
    with open(file.file_path, "rb") as f:
        yield from f
