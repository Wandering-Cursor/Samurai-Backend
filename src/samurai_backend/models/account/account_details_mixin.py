import pydantic

from samurai_backend.account.get.account import get_account
from samurai_backend.account.schemas.account import AccountRepresentation, AccountSearchSchema
from samurai_backend.db import get_db_session
from samurai_backend.models.account.account import AccountModel


class AccountDetailsMixin(pydantic.BaseModel):
    @property
    def _account_id(self: "AccountDetailsMixin") -> pydantic.UUID4:
        raise NotImplementedError("Please implement _account_id to use AccountDetailsMixin")

    @property
    def _account(self: "AccountDetailsMixin") -> AccountModel:
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
