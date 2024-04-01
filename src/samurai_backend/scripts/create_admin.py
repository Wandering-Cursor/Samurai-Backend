from samurai_backend.core.operations import store_entity
from samurai_backend.db import get_db_session
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.account_permission import AccountPermission


def create_admin() -> None:
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    db_generator = get_db_session()
    db = next(db_generator)
    admin = AccountModel(
        email=email,
        username=email,
        first_name="Admin",
        last_name="Admin",
        registration_code=None,
        is_email_verified=True,
        permissions=[
            AccountPermission(name="admin"),
        ],
        account_type="admin",
    )
    admin.set_password(password)

    store_entity(db, admin)
    print(f"Admin account created with email: {email}")  # noqa: T201


if __name__ == "__main__":
    create_admin()
