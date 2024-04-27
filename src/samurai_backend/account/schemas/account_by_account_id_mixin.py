import pydantic

from samurai_backend.account.schemas.account_details_mixin import AccountDetailsMixin


class AccountByAccountIdMixin(AccountDetailsMixin):
    account_id: pydantic.UUID4

    @property
    def _account_id(self: "AccountByAccountIdMixin") -> pydantic.UUID4:
        return self.account_id
