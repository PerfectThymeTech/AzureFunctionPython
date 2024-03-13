import logging
from logging import Logger

# from azure.identity import ManagedIdentityCredential
from azure.monitor.opentelemetry.exporter import (
    ApplicationInsightsSampler,
    AzureMonitorLogExporter,
    AzureMonitorMetricExporter,
    AzureMonitorTraceExporter,
)
from fastapi import FastAPI
from core.config import settings
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Tracer, set_tracer_provider


def setup_logging(module) -> Logger:
    """Setup logging and event handler.

    RETURNS (Logger): The logger object to log activities.
    """
    logger = logging.getLogger(module)
    logger.setLevel(settings.LOGGING_LEVEL)
    logger.propagate = False

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
        resource = Resource.create(
            {
                "service.name": settings.WEBSITE_NAME,
                "service.namespace": settings.WEBSITE_NAME,
                "service.instance.id": settings.WEBSITE_INSTANCE_ID,
            }
        )

        # Create logger provider
        logger_exporter = AzureMonitorLogExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(
                exporter=logger_exporter,
                schedule_delay_millis=settings.LOGGING_SCHEDULE_DELAY,
            )
        )
        set_logger_provider(logger_provider)
        handler = LoggingHandler(
            level=settings.LOGGING_LEVEL, logger_provider=logger_provider
        )
        logging.getLogger().addHandler(handler)

        # Create tracer provider
        tracer_exporter = AzureMonitorTraceExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        sampler = ApplicationInsightsSampler(
            sampling_ratio=settings.LOGGING_SAMPLING_RATIO
        )
        tracer_provider = TracerProvider(resource=resource, sampler=sampler)
        tracer_provider.add_span_processor(
            BatchSpanProcessor(
                span_exporter=tracer_exporter,
                schedule_delay_millis=settings.LOGGING_SCHEDULE_DELAY,
            )
        )
        set_tracer_provider(tracer_provider)

        # Create meter provider
        metrics_exporter = AzureMonitorMetricExporter.from_connection_string(
            settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            # credential=credential
        )
        reader = PeriodicExportingMetricReader(
            exporter=metrics_exporter,
            export_interval_millis=settings.LOGGING_SCHEDULE_DELAY,
        )
        meter_provider = MeterProvider(metric_readers=[reader], resource=resource)
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
            excluded_urls=f".*.in.applicationinsights.azure.com/.*,{settings.API_V1_STR}/health/heartbeat",
            tracer_provider=tracer_provider,
            meter_provider=meter_provider,
        )
        HTTPXClientInstrumentor().instrument()
        SystemMetricsInstrumentor(config=system_metrics_config).instrument()
