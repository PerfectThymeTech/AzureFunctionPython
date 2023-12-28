import logging
from logging import Logger

from azure.monitor.opentelemetry import configure_azure_monitor

# from azure.identity import ManagedIdentityCredential
from fastapi import FastAPI
from fastapp.core.config import settings
from opentelemetry import trace
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.trace import Tracer


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

        # Configure azure monitor exporter
        configure_azure_monitor(
            connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
            disable_offline_storage=False,
            # credential=credential,
        )

        # Configure custom metrics
        system_metrics_config = {
            "system.memory.usage": ["used", "free", "cached"],
            "system.cpu.time": ["idle", "user", "system", "irq"],
            "system.network.io": ["transmit", "receive"],
            "process.runtime.memory": ["rss", "vms"],
            "process.runtime.cpu.time": ["user", "system"],
        }

        # Create instrumenter
        AioHttpClientInstrumentor().instrument()
        SystemMetricsInstrumentor(config=system_metrics_config).instrument()
