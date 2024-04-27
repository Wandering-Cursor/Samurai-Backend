import pydantic

from .account import account_representation


class StudentRepresentation(account_representation):
    group_id: pydantic.UUID4
