import json
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import (
    get_swagger_ui_oauth2_redirect_html,
    swagger_ui_default_parameters,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from samurai_backend.account.router import account_router
from samurai_backend.admin.router import admin_router
from samurai_backend.communication.router import communication_router
from samurai_backend.core.router import auth_router, common_router, ws_router
from samurai_backend.error_handlers import add_error_handlers
from samurai_backend.log import main_logger
from samurai_backend.middleware import add_cors_middleware, add_gzip_middleware
from samurai_backend.otel import setup_otel
from samurai_backend.settings import settings
from samurai_backend.user_projects.router import stats_projects_router, user_projects_router

dev_server = {
    "url": "http://localhost:8000",
    "description": "Local development server",
}

servers = []
if settings.debug:
    servers.append(dev_server)

servers += [
    {
        "url": "https://api.obscurial.art",
        "description": "Production server",
    },
]


async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    main_logger.info("Starting up...")

    main_logger.debug("Mounting static files")
    fastapi_app.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static",
    )

    main_logger.debug("Including routers")
    fastapi_app.include_router(auth_router)
    fastapi_app.include_router(ws_router)
    fastapi_app.include_router(admin_router)
    fastapi_app.include_router(account_router)
    user_projects_router.include_router(stats_projects_router)
    fastapi_app.include_router(user_projects_router)
    fastapi_app.include_router(communication_router)
    fastapi_app.include_router(common_router)

    yield

    main_logger.info("Shutting down...")


app = FastAPI(
    debug=settings.debug,
    title="Samurai Backend",
    summary="Backend for the Samurai project",
    version=settings.app_version,
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
    servers=servers,
    lifespan=lifespan,
)

# Has to be outside the lifecycle function
main_logger.debug("Adding error handlers")
add_error_handlers(app)
add_cors_middleware(app)
add_gzip_middleware(app)
setup_otel(app)


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
async def custom_swagger_ui_html() -> HTMLResponse:
    openapi_url = app.openapi_url
    title = app.title + " - Swagger UI"
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    swagger_js_url = "/static/swagger-ui-bundle.js"
    swagger_css_url = "/static/swagger-ui.css"
    swagger_ui_parameters = app.swagger_ui_parameters
    swagger_favicon_url = "/static/favicon.png"

    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}" nonce="{settings.script_nonce}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script nonce="{settings.script_nonce}">
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


if app.swagger_ui_oauth2_redirect_url:

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()


@app.get(
    "/redoc",
    include_in_schema=False,
)
async def custom_redoc_html() -> HTMLResponse:
    """
    Generate and return the HTML response that loads ReDoc for the alternative
    API docs (normally served at `/redoc`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load ReDoc's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    openapi_url = app.openapi_url
    title = app.title + " - ReDoc"
    redoc_js_url = "/static/redoc.standalone.js"
    redoc_favicon_url = "/static/favicon.png"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style nonce="{settings.script_nonce}">
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="{openapi_url}" nonce="{settings.script_nonce}"></redoc>
    <script src="{redoc_js_url}" nonce="{settings.script_nonce}"></script>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.get(
    "/health",
)
async def health() -> dict[str, str]:
    return {"status": "ok"}
