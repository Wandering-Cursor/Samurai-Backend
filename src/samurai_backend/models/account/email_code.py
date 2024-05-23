import datetime
import uuid

import sqlmodel

from samurai_backend.enums.email_code_type import EmailCodeType
from samurai_backend.models.base import BaseModel
from samurai_backend.utils import hashes
from samurai_backend.utils.current_time import current_time

timedelta_for_email_codes = {
    EmailCodeType.RESET_PASSWORD: datetime.timedelta(minutes=30),
}


def timedelta_for_code_type(code_type: EmailCodeType) -> datetime.timedelta:
    return timedelta_for_email_codes.get(code_type, datetime.timedelta(hours=1))


class EmailCodeModel(BaseModel, table=True):
    email_code_id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    account_id: uuid.UUID = sqlmodel.Field(
        nullable=False,
        foreign_key="accountmodel.account_id",
    )
    code_type: EmailCodeType = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.Enum(EmailCodeType),
            nullable=False,
        ),
    )

    hashed_code_value: str = sqlmodel.Field(
        nullable=False,
    )
    is_used: bool = sqlmodel.Field(
        default=False,
    )

    expiration_date: datetime.datetime = sqlmodel.Field(
        nullable=False,
        sa_type=sqlmodel.DateTime(timezone=True),
    )

    def set_value(self: "EmailCodeModel", value: str | None = None) -> str:
        """If value is not specified, a random string will be generated."""
        if value is None:
            value = hashes.generate_random_string(length=12)

        self.hashed_code_value = self.get_hashed_value(value)

        return value

    def check_value(self: "EmailCodeModel", value: str) -> bool:
        return hashes.check_hash(
            value=value,
            hashed_value=self.hashed_code_value,
        )

    def set_expiration_date(self: "EmailCodeModel") -> None:
        self.expiration_date = self.get_expiration_date

    @property
    def get_expiration_date(self: "EmailCodeModel") -> datetime.datetime:
        return current_time() + timedelta_for_code_type(self.code_type)

    @property
    def is_expired(self: "EmailCodeModel") -> bool:
        return self.expiration_date < current_time()

    @staticmethod
    def get_hashed_value(value: str) -> str:
        return hashes.hash_value(value)
