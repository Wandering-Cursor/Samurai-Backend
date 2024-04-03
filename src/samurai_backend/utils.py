import datetime
from typing import TYPE_CHECKING

from passlib.context import CryptContext
from sqlalchemy import func
from sqlmodel import Session
from sqlmodel.sql.expression import SelectOfScalar

from samurai_backend.settings import settings

if TYPE_CHECKING:
    from samurai_backend.models.base import BaseModel

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


def current_time() -> datetime.datetime:
    return datetime.datetime.now(tz=settings.timezone)


def update_time(
    mapper: object,  # noqa
    connection: object,  # noqa
    target: "BaseModel",
) -> None:
    target.updated_at = current_time()
