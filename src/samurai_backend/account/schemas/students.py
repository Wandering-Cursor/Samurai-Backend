import pydantic

from .account import account_representation


class StudentRepresentation(account_representation.AccountRepresentation):
    group_id: pydantic.UUID4
