from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from sqlmodel import Session

from samurai_backend.account.get.account import get_account
from samurai_backend.db import get_db_session_async
from samurai_backend.dependencies.oauth2_scheme import oauth2_scheme
from samurai_backend.models.account.account import AccountModel
from samurai_backend.schemas import TokenData
from samurai_backend.settings import security_settings


def get_current_account(
    db: Annotated[Session, Depends(get_db_session_async)],
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AccountModel:
    """
    Returns the current account from the database.
    """
    from samurai_backend.account.schemas.account.account import AccountSearchSchema

    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(
            token,
            security_settings.secret_key,
            algorithms=[security_settings.algorithm],
        )
        account_id = payload.get("sub")
        if not isinstance(account_id, str):
            raise JWTError

        token_type = payload.get("type")
        if not isinstance(token_type, str) or token_type != "access":
            raise JWTError

        token_scopes = payload.get("scopes", [])
        if not isinstance(token_scopes, list):
            raise JWTError

        token_data = TokenData(
            sub=account_id,
            scopes=token_scopes,
        )
    except JWTError as e:
        raise credentials_exception from e

    account = get_account(
        session=db,
        search=AccountSearchSchema(
            account_id=token_data.sub,
        ),
    )
    if account is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        is_scope_specific = ":" in scope
        general_scope = scope.split(":")[0] if is_scope_specific else scope

        if scope in token_data.scopes:
            continue
        if general_scope in token_data.scopes:
            continue

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return account
