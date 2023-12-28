import logging
from logging import Logger

# from azure.identity import ManagedIdentityCredential
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorMetricExporter,
    AzureMonitorTraceExporter,
    AzureMonitorLogExporter,
)
from fastapi import FastAPI
from fastapp.core.config import settings
from opentelemetry import trace
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Tracer
from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
    set_logger_provider,
)
from opentelemetry.metrics import set_meter_provider
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

def setup_logging(module) -> Logger:
    """Setup logging and event handler.

    RETURNS (Logger): The logger object to log activities.
    """
    logger = logging.getLogger(module)
    logger.setLevel(settings.LOGGING_LEVEL)
    logger.propagate = False

    # Create logging handler
    logging_handler = LoggingHandler()
    logger.addHandler(logging_handler)

    # Create stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)-8.8s] %(message)s")
    )
    logger.addHandler(stream_handler)
    return logger


def setup_tracer(module) -> Tracer:
    """Setup tracer and event handler.

    RETURNS (Tracer): The tracer object to create spans.
    """
    tracer = trace.get_tracer(module)
    return tracer


def setup_opentelemetry(app: FastAPI):
    """Setup tracer for Open Telemetry.

    app (FastAPI): The app to be instrumented by Open Telemetry.
    RETURNS (None): Nothing is being returned.
    """
    if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
        # credential = ManagedIdentityCredential()

        # Create logger provider
        logger_exporter = AzureMonitorLogExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        logger_provider = LoggerProvider()
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(logger_exporter))
        set_logger_provider(logger_provider)

        # Create tracer provider
        tracer_exporter = AzureMonitorTraceExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        tracer_provider = TracerProvider(resource=Resource({SERVICE_NAME: "api"}))
        set_tracer_provider(tracer_provider)
        get_tracer_provider().add_span_processor(BatchSpanProcessor(tracer_exporter))

        # Create meter provider
        metrics_exporter = AzureMonitorMetricExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        reader = PeriodicExportingMetricReader(
            metrics_exporter, export_interval_millis=5000
        )
        meter_provider = MeterProvider(metric_readers=[reader])
        set_meter_provider(meter_provider)
        
        # Configure custom metrics
        system_metrics_config = {
            "system.memory.usage": ["used", "free", "cached"],
            "system.cpu.time": ["idle", "user", "system", "irq"],
            "system.network.io": ["transmit", "receive"],
            "process.runtime.memory": ["rss", "vms"],
            "process.runtime.cpu.time": ["user", "system"],
        }

        # Create instrumenter
        FastAPIInstrumentor.instrument_app(
            app,
            excluded_urls=f"{settings.API_V1_STR}/health/heartbeat",
            tracer_provider=tracer_provider,
            meter_provider=meter_provider,
        )
        AioHttpClientInstrumentor().instrument(tracer_provider=tracer_provider)
        SystemMetricsInstrumentor(config=system_metrics_config).instrument()
