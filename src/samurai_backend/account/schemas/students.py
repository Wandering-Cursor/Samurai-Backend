import pydantic

from .account import AccountRepresentation


class StudentRepresentation(AccountRepresentation):
    group_id: pydantic.UUID4
