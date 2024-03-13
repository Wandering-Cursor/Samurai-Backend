from sqlalchemy import UUID, Column, String

from samurai_backend.db import Base


class BaseModel(Base):
    __tablename__ = "BaseModel"

    id = Column(UUID, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
