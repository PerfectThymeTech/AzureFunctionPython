import logging
from logging import Logger

from fastapp.core.config import settings
from opencensus.extension.azure.functions import OpenCensusExtension

if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
    OpenCensusExtension.configure()


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
