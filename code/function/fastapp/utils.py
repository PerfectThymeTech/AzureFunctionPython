import logging
from logging import Logger

# from azure.identity import ManagedIdentityCredential
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorMetricExporter,
    AzureMonitorTraceExporter,
)
from fastapi import FastAPI
from fastapp.core.config import settings
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
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


def setup_opentelemetry(app: FastAPI):
    """Setup tracer and metrics for Open Telemetry.
    app (FastAPI): The app to be instrumented by Open Telemetry.
    RETURNS (None): Nothing is being returned.
    """
    if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
        # credential = ManagedIdentityCredential()

        # Create tracer provider
        tracer_exporter = AzureMonitorTraceExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        tracer_provider = TracerProvider(resource=Resource({SERVICE_NAME: "api"}))
        tracer_provider.add_span_processor(BatchSpanProcessor(tracer_exporter))

        # Create meter provider
        metrics_exporter = AzureMonitorMetricExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        reader = PeriodicExportingMetricReader(
            metrics_exporter, export_interval_millis=5000
        )
        meter_provider = MeterProvider(metric_readers=[reader])

        # Create instrumenter
        FastAPIInstrumentor.instrument_app(
            app,
            excluded_urls=f"{settings.API_V1_STR}/health/heartbeat",
            tracer_provider=tracer_provider,
            meter_provider=meter_provider,
        )
        AioHttpClientInstrumentor().instrument(tracer_provider=tracer_provider)
