from samurai_backend.models.account.account import BaseAccountModel
from samurai_backend.models.account.account_permission import AccountPermission
from samurai_backend.models.account.connection import ConnectionModel
from samurai_backend.models.account.registration_code import RegistrationEmailCode


class AccountModelSchema(BaseAccountModel):
    permissions: list[AccountPermission]
    connections: list[ConnectionModel]
    registration_email_code: RegistrationEmailCode | None
