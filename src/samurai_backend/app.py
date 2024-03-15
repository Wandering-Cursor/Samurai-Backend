from fastapi import FastAPI

from samurai_backend.core.router import auth_router
from samurai_backend.db import create_all_tables
from samurai_backend.middleware import add_cors_middleware
from samurai_backend.settings import settings

app = FastAPI(
    debug=settings.debug,
    title="Samurai Backend",
    summary="Backend for the Samurai project",
    version="0.7.0",
)

add_cors_middleware(app)

create_all_tables()


app.include_router(auth_router)
