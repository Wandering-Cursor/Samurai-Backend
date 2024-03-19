from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

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
    docs_url=None,
    redoc_url=None,
)


app.mount("/static", StaticFiles(directory="static"), name="static")

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


@app.get(
    "/docs",
    include_in_schema=False,
)
async def custom_swagger_ui_html() -> str:
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect() -> HTMLResponse:
    return get_swagger_ui_oauth2_redirect_html()


@app.get(
    "/redoc",
    include_in_schema=False,
)
async def custom_redoc_html() -> str:
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
