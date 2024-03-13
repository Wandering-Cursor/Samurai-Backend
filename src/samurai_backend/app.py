from collections.abc import Generator
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI

from samurai_backend.core import get, schemas
from samurai_backend.db import Base, SessionLocal, engine
from samurai_backend.middleware import add_cors_middleware
from samurai_backend.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# TODO: Investigate why this is necessary
Base.metadata.create_all(bind=engine)


# TODO: Move to db.py and dependencies.py
def get_db() -> Generator["Session", None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    debug=settings.debug,
    title="Samurai Backend",
    summary="Backend for the Samurai project",
    version="0.7.0",
)

add_cors_middleware(app)


@app.get("/")
async def get_bases(
    db: Annotated["Session", Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.BaseModel]:
    return get.get_bases(db, skip, limit)


@app.post("/")
async def insert_base(
    db: Annotated["Session", Depends(get_db)],
    base: schemas.BaseModel,
) -> schemas.BaseModel:
    return get.insert_base(db, base)
