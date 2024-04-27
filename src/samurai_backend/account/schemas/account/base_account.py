import pydantic

from samurai_backend.core.schemas import BaseSchema


class BaseAccount(BaseSchema):
    account_id: pydantic.UUID4
    email: pydantic.EmailStr
