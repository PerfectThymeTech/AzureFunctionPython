import logging
from logging import Logger

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from fastapi import FastAPI
from fastapp.core.config import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_logging(module) -> Logger:
    """Setup logging and event handler.

    RETURNS (Logger): The logger object to log activities.
    """
    logger = logging.getLogger(module)
    logger.setLevel(settings.LOGGING_LEVEL)
    logger.propagate = False

    # Create stream handler
    logger_stream_handler = logging.StreamHandler()
    logger_stream_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)-8.8s] %(message)s")
    )
    logger.addHandler(logger_stream_handler)
    return logger


def setup_tracer(app: FastAPI):
    """Setup tracer for Open Telemetry.

    app (FastAPI): The app to be instrumented by Open Telemetry.
    RETURNS (None): Nothing is being returned.
    """
    if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
        exporter = AzureMonitorTraceExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING
        )
        tracer = TracerProvider(resource=Resource({SERVICE_NAME: "api"}))
        tracer.add_span_processor(BatchSpanProcessor(exporter))
        FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
