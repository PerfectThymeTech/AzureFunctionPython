import logging

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "FunctionSample"
    SERVER_NAME: str = "FunctionSample"
    APP_VERSION: str = "v0.0.1"
    API_V1_STR: str = "/v1"
    LOGGING_LEVEL: int = logging.INFO
    DEBUG: bool = False
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = Field(
        default="", env="APPLICATIONINSIGHTS_CONNECTION_STRING"
    )


settings = Settings()
