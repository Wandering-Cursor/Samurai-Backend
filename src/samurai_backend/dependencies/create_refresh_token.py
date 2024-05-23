import secrets
from datetime import datetime, timedelta

from jose import jwt

from samurai_backend.schemas import TokenData
from samurai_backend.settings import security_settings, settings


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
