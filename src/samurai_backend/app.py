from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from samurai_backend.account.router import account_router
from samurai_backend.admin.router import admin_router
from samurai_backend.core.router import auth_router
from samurai_backend.error_handlers import add_error_handlers
from samurai_backend.middleware import add_cors_middleware
from samurai_backend.settings import settings

app = FastAPI(
    debug=settings.debug,
    title="Samurai Backend",
    summary="Backend for the Samurai project",
    version="0.7.0",
    swagger_ui_parameters={
        "defaultModelRendering": "model",
        "displayRequestDuration": True,
        "docExpansion": "none",
        "filter": "",
        "operationsSorter": "alpha",
        "tagsSorter": "alpha",
    },
)

add_error_handlers(app)
add_cors_middleware(app)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(account_router)


@app.get(
    "/",
    include_in_schema=False,
)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse("/docs")
