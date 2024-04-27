from samurai_backend.account.schemas.account.base_account import BaseAccount


class AccountRepresentation(BaseAccount):
    username: str

    first_name: str
    middle_name: str | None = None
    last_name: str
