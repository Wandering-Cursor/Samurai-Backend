from samurai_backend.utils.pwd_context import pwd_context


def get_password_hash(salt: str, password: str) -> str:
    """
    Returns a hashed password.
    """
    return pwd_context.hash(password + salt)
