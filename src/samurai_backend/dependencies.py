import secrets
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from sqlmodel import Session

from samurai_backend.account.get.account import get_account
from samurai_backend.core.schemas import TokenData
from samurai_backend.db import get_db_session_async
from samurai_backend.enums import Permissions
from samurai_backend.models.account.account import AccountModel
from samurai_backend.settings import security_settings, settings

database_session_type = Session
database_session = get_db_session_async

account_type = AccountModel


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token/form",
    scopes={permission.value: permission.description for permission in Permissions},
    description=(
        "Scopes cannot be issued per token (at the moment).\n"
        "User can be assigned a scope, which is stored in the database.\n"
        "If you have a scope with no : in it, it is a general scope.\n"
        "If you have a scope with a : in it, it is a specific scope.\n"
        "If you have a general scope, you can perform all actions of this scope.\n"
    ),
)


def create_access_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    """
    Creates an access token.
    """
    to_encode = data.model_dump(mode="json")

    iat = datetime.now(tz=settings.timezone)
    if expires_delta:
        expire = iat + expires_delta
    else:
        expire = iat + timedelta(minutes=security_settings.access_token_lifetime_minutes)
    to_encode.update({"exp": int(expire.timestamp())})
    to_encode.update({"iat": int(iat.timestamp())})
    to_encode.update({"type": "access"})

    to_encode.update({"jti": secrets.token_urlsafe(32)})

    return jwt.encode(
        to_encode,
        security_settings.secret_key,
        algorithm=security_settings.algorithm,
    )


def create_refresh_token(data: TokenData) -> str:
    """
    Creates a refresh token.
    """
    to_encode = data.model_dump(mode="json")

    iat = datetime.now(tz=settings.timezone)
    expire = iat + timedelta(minutes=security_settings.refresh_token_lifetime_minutes)

    to_encode.update({"exp": int(expire.timestamp())})
    to_encode.update({"iat": int(iat.timestamp())})
    to_encode.update({"type": "refresh"})

    # Add entropy to the token to reduce the chance of a collision.
    to_encode.update({"jti": secrets.token_urlsafe(32)})

    return jwt.encode(
        to_encode,
        security_settings.secret_key,
        algorithm=security_settings.algorithm,
    )


def decode_refresh_token(token: str) -> TokenData:
    """
    Decodes a refresh token.
    """
    token_data = TokenData(
        **jwt.decode(
            token,
            security_settings.secret_key,
            algorithms=[security_settings.algorithm],
        )
    )
    if token_data.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    return token_data


def get_current_account(
    db: Annotated[Session, Depends(database_session)],
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> account_type:
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


def get_current_active_account(
    current_account: Annotated[
        account_type,
        Security(
            get_current_account,
            scopes=[],
        ),
    ],
) -> account_type:
    """
    Returns the current active account.
    """
    if current_account.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
        )
    if current_account.is_email_verified is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
        )

    return current_account


def ws_get_current_active_account(
    session: Annotated[Session, Depends(database_session)],
    token: Annotated[str, Header(alias="Authorization")],
    security_scopes: SecurityScopes,
) -> account_type:
    """
    Returns the current active account.
    """
    token = token.replace("Bearer ", "")

    current_account = get_current_account(
        db=session,
        security_scopes=security_scopes,
        token=token,
    )
    return get_current_active_account(current_account)
