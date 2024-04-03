from samurai_backend.admin.get.permissions import get_permissions
from samurai_backend.core.operations import store_entity
from samurai_backend.db import get_db_session
from samurai_backend.enums import AccountType, Permissions
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.account.account_permission import AccountPermission


def create_admin() -> None:
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    db_generator = get_db_session()
    db = next(db_generator)
    all_permissions = get_permissions(db)
    admin_permission = next(
        (
            permission
            for permission in all_permissions
            if permission.name == Permissions.ADMIN.value
        ),
        None,
    )
    if not admin_permission:
        admin_permission = AccountPermission(
            name=Permissions.ADMIN.value,
        )

    admin = AccountModel(
        email=email,
        username=email,
        first_name="Admin",
        last_name="Admin",
        registration_code=None,
        is_email_verified=True,
        permissions=[
            admin_permission,
        ],
        account_type=AccountType.ADMIN,
    )
    admin.set_password(password)

    store_entity(db, admin)
    print(f"Admin account created with email: {email}")  # noqa: T201


if __name__ == "__main__":
    create_admin()
