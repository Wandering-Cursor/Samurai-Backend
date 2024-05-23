import pydantic

from samurai_backend.schemas import BaseSchema


class BaseAccount(BaseSchema):
    account_id: pydantic.UUID4
    email: pydantic.EmailStr
