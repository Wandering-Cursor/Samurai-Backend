from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from samurai_backend.settings import security_settings


def add_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=security_settings.cors_allow_origins,
        allow_origin_regex=security_settings.cors_allow_origin_regex,
        allow_credentials=security_settings.cors_allow_credentials,
        allow_methods=security_settings.cors_allow_methods,
        allow_headers=security_settings.cors_allow_headers,
        expose_headers=[
            "Content-Disposition",
            "content-disposition",
            "content-type",
            "Content-Type",
        ],
    )


def add_gzip_middleware(app: FastAPI) -> None:
    app.add_middleware(
        GZipMiddleware,
    )


# For future:
# Consider creating a middleware that will log all requests and responses
# Consider creating a middleware that will log request times
#   (averaged over a period of time for each endpoint, to add monitoring)
