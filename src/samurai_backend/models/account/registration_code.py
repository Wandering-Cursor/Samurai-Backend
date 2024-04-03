import secrets
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from samurai_backend.models.base import BaseModel

if TYPE_CHECKING:
    from .account import AccountModel


def generate_registration_code() -> str:
    return secrets.token_urlsafe(16)


class RegistrationEmailCode(BaseModel, table=True):
    account_id: uuid.UUID = Field(
        description="To which account the registration code belongs to.",
        foreign_key="accountmodel.account_id",
        primary_key=True,
    )

    # Security suggest us to hash the code
    # In this system, it's acceptable to not do so
    # If you are upgrading this system's security, please hash the code
    # Basic idea is - since accounts are created by the administration - we may as well let them
    # know the code in plain text
    code: str = Field(
        default_factory=generate_registration_code,
        description="The registration code, used to verify the email.",
        unique=True,
    )

    is_used: bool = Field(
        description="If the code has been used.",
        default=False,
    )

    account: "AccountModel" = Relationship(back_populates="registration_email_code")
