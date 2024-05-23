from fastapi import HTTPException, status
from jose import jwt

from samurai_backend.schemas import TokenData
from samurai_backend.settings import security_settings


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
