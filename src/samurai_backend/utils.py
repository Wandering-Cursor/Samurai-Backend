from passlib.context import CryptContext
from sqlalchemy import func
from sqlmodel import Session
from sqlmodel.sql.expression import SelectOfScalar

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


def get_count(session: Session, q: SelectOfScalar) -> int:
    count_q = q.with_only_columns(func.count()).order_by(None).select_from(*q.froms)
    iterator = session.exec(count_q)
    for count in iterator:
        return count
    return 0
