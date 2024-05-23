from samurai_backend.account.schemas.account.base_account import BaseAccount
from samurai_backend.enums.account_type import AccountType


class AccountRepresentation(BaseAccount):
    username: str

    first_name: str
    middle_name: str | None = None
    last_name: str

    account_type: AccountType
