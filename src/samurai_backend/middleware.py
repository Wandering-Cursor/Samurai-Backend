from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from samurai_backend.settings import security_settings


def add_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=security_settings.cors_allow_origins,
        allow_credentials=security_settings.cors_allow_credentials,
        allow_methods=security_settings.cors_allow_methods,
        allow_headers=security_settings.cors_allow_headers,
    )
