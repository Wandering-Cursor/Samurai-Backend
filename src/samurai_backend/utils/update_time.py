from typing import TYPE_CHECKING

from samurai_backend.utils.current_time import current_time

if TYPE_CHECKING:
    from samurai_backend.models.base import BaseModel


def update_time(
    mapper: object,  # noqa
    connection: object,  # noqa
    target: "BaseModel",
) -> None:
    target.updated_at = current_time()
