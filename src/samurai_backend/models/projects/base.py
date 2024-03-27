from sqlmodel import Field, SQLModel


class BaseNamed(SQLModel):
    name: str = Field(description="Name of an object")
    description: str | None = Field(
        default=None,
        nullable=True,
        description="Description of an object (optional)",
    )
