from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def verify_password(salt: str, plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password + salt, hashed_password)


def get_password_hash(salt: str, password: str) -> str:
    """
    Returns a hashed password.
    """
    return pwd_context.hash(password + salt)
