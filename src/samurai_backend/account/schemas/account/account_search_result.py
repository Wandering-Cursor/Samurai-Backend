from samurai_backend.models.account.account import AccountModel
from samurai_backend.schemas import BasePaginatedResponse


class AccountSearchResult(BasePaginatedResponse):
    content: list[AccountModel]
