import pydantic

from samurai_backend.models.account.account import AccountModel

from .account.account import AccountRepresentation, AccountSearchSchema


class AccountDetailsMixin(pydantic.BaseModel):
    @property
    def _account_id(self: "AccountDetailsMixin") -> pydantic.UUID4:
        raise NotImplementedError("Please implement _account_id to use AccountDetailsMixin")

    @property
    def _account(self: "AccountDetailsMixin") -> AccountModel:
        from samurai_backend.account.get.account import get_account
        from samurai_backend.db import get_db_session

        generator = get_db_session()
        session = next(generator)
        account = get_account(session, search=AccountSearchSchema(account_id=self._account_id))
        if not account:
            raise ValueError("Account not found.")

        return account

    @pydantic.computed_field
    @property
    def account_details(self: "AccountDetailsMixin") -> AccountRepresentation:
        return AccountRepresentation.model_validate(
            self._account,
            from_attributes=True,
        )


class AccountByAccountIdMixin(AccountDetailsMixin):
    account_id: pydantic.UUID4

    @property
    def _account_id(self: "AccountByAccountIdMixin") -> pydantic.UUID4:
        return self.account_id
