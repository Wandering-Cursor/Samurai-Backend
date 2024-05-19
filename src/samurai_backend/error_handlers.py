import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose.exceptions import JOSEError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


def validation_exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
    errors = exc.errors()
    for error in errors:
        ctx = error.get("ctx", {})
        if "error" in ctx and isinstance(ctx["error"], ValueError):
            ctx["error"] = str(ctx["error"])

    raise HTTPException(
        status_code=422,
        detail=errors,
        headers={
            "X-Error": "Validation Error",
        },
    )


def jose_exception_handler(_: Request, exc: JOSEError) -> JSONResponse:
    logging.exception(exc.__cause__, exc_info=True)
    logging.exception(str(exc), exc_info=True)
    raise HTTPException(
        detail={
            "detail": "Unauthorized",
        },
        status_code=401,
        headers={
            "X-Error": "JOSE Error",
        },
    )


def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    logging.exception(exc.__cause__, exc_info=True)
    logging.exception(str(exc), exc_info=True)
    return JSONResponse(
        content={
            "detail": exc.detail,
        },
        status_code=exc.status_code,
        headers={
            "X-Error": "HTTP Error",
            **(exc.headers or {}),
        },
    )


def any_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logging.error(exc, exc_info=True)
    return JSONResponse(
        content={
            "detail": "Internal Server Error",
        },
        status_code=500,
        headers={
            "X-Error": "Server Error",
        },
    )


def add_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(JOSEError, jose_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(SQLAlchemyError, any_exception_handler)
    app.add_exception_handler(Exception, any_exception_handler)
