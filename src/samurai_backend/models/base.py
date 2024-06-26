import datetime

import sqlalchemy as sa
import sqlmodel
from sqlalchemy.event import listen

from samurai_backend.utils.current_time import current_time


class BaseModel(sqlmodel.SQLModel):
    created_at: datetime.datetime = sqlmodel.Field(
        default_factory=current_time,
        nullable=True,
        sa_type=sa.DateTime(timezone=True),
    )
    updated_at: datetime.datetime = sqlmodel.Field(
        default_factory=current_time,
        nullable=True,
        sa_type=sa.DateTime(timezone=True),
    )

    def update_time(self) -> None:
        self.updated_at = current_time()


listen(BaseModel, "before_update", current_time)
