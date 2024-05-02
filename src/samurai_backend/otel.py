import os
from typing import TYPE_CHECKING

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from samurai_backend.settings import settings

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_env() -> None:
    os.environ["OTEL_PYTHON_FASTAPI_EXCLUDED_URLS"] = "/health,/,/docs,/redoc"
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE"] = ".*"
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE"] = "Content.*,X-.*"
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SANITIZE_FIELDS"] = (
        ".*session.*,set-cookie,authorization,proxy-authorization"
    )


def setup_otel(app: "FastAPI") -> None:
    setup_env()

    resource = Resource(
        attributes={
            "service.name": "Samurai-Backend",
            "service.version": app.version,
            "deployment.environment": "production",
            "service.namespace": "samurai",
            # From Grafana
            "service.instance.id": "shopping-cart-66b6c48dd5-hprdn",
        }
    )
    trace_provider = TracerProvider(resource=resource)

    headers = {"Authorization": settings.otel_auth_header} if settings.otel_auth_header else {}
    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=settings.otel_exporter_endpoint,
            headers=headers,
            insecure=True,
        )
    )

    trace_provider.add_span_processor(processor)
    trace.set_tracer_provider(trace_provider)

    LoggingInstrumentor().instrument(set_logging_format=True)
    PsycopgInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    FastAPIInstrumentor.instrument_app(app)
