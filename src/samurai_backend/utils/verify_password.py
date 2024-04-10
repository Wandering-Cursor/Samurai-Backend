from samurai_backend.utils.pwd_context import pwd_context


def verify_password(salt: str, plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password + salt, hashed_password)
