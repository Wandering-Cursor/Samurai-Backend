import importlib

from fastapi.security import OAuth2PasswordBearer

permissions_module = importlib.import_module("samurai_backend.enums.permissions")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token/form",
    scopes={
        permission.value: permission.description for permission in permissions_module.Permissions
    },
    description=(
        "Scopes cannot be issued per token (at the moment).\n"
        "User can be assigned a scope, which is stored in the database.\n"
        "If you have a scope with no : in it, it is a general scope.\n"
        "If you have a scope with a : in it, it is a specific scope.\n"
        "If you have a general scope, you can perform all actions of this scope.\n"
    ),
)
