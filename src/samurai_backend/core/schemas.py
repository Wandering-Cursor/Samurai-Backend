import uuid

import pydantic


class BaseModel(pydantic.BaseModel):
    id: pydantic.UUID4 = pydantic.Field(default_factory=uuid.uuid4)
    name: str

    class Config:
        from_attributes = True
