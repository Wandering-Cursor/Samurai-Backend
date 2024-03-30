from samurai_backend.account.get.account import get_account
from samurai_backend.account.schemas.account import AccountSearchSchema
from samurai_backend.core.operations import update_entity
from samurai_backend.db import get_db_session


def change_password() -> None:
    username = input("Enter email/username: ")
    password = input("Enter new password: ")

    db_generator = get_db_session()
    db = next(db_generator)
    account = get_account(
        db,
        AccountSearchSchema(
            username=username,
            email=username,
        ),
    )
    if not account:
        print(f"Could not find account with email: {username}")  # noqa: T201
        return

    account.set_password(password)

    update_entity(db, account, primary_key="account_id")
    print(f"Password changed for account with email/username: {username}")  # noqa: T201


if __name__ == "__main__":
    change_password()
