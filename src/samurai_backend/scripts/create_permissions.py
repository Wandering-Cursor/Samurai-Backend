# ruff: noqa: T201

from samurai_backend.core.operations import store_entity
from samurai_backend.db import get_db_session
from samurai_backend.enums import Permissions
from samurai_backend.errors import SamuraiIntegrityError
from samurai_backend.models.account.account_permission import AccountPermission
from samurai_backend.scripts._base import colored_print


def create_default_permissions() -> None:
    for permission in Permissions:
        db_generator = get_db_session()
        session = next(db_generator)

        entity = AccountPermission(
            name=permission.value,
            description=f"Default: {permission.value}",
        )
        try:
            store_entity(session, entity)
        except SamuraiIntegrityError:
            colored_print(f"Permission already exists: {permission.name}", "warning")
            continue

        colored_print(f"Permission created: {permission.name}", "info")

    colored_print("Default permissions created.", "success")


if __name__ == "__main__":
    create_default_permissions()
