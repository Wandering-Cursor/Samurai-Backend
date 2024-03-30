from samurai_backend.core.schemas import BasePaginatedResponse
from samurai_backend.models.account.account import AccountModel


class AccountSearchResult(BasePaginatedResponse):
    content: list[AccountModel]
