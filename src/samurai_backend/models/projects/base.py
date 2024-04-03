from sqlmodel import Field

from samurai_backend.models.base import BaseModel


class BaseNamed(BaseModel):
    name: str = Field(description="Name of an object")
    description: str | None = Field(
        default=None,
        nullable=True,
        description="Description of an object (optional)",
    )
