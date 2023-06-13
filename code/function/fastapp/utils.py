import logging
from logging import Logger

from fastapp.core.config import settings
from opencensus.ext.azure.log_exporter import AzureLogHandler


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

    # Add azure event handler
    if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
        azure_log_handler = AzureLogHandler()
        azure_log_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(module)-8.8s] %(message)s"
            )
        )
        logger.addHandler(azure_log_handler)

    return logger
