import logging

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FunctionSample"
    SERVER_NAME: str = "FunctionSample"
    APP_VERSION: str = "v0.0.1"
    API_V1_STR: str = "/v1"
    LOGGING_LEVEL: int = logging.INFO
    LOGGING_SAMPLING_RATIO: float = 1.0
    LOGGING_SCHEDULE_DELAY: int = 5000
    DEBUG: bool = False
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = Field(
        default="", env="APPLICATIONINSIGHTS_CONNECTION_STRING"
    )
    WEBSITE_NAME: str = Field(default="test", env="WEBSITE_SITE_NAME")
    WEBSITE_INSTANCE_ID: str = Field(default="0", env="WEBSITE_INSTANCE_ID")
    MY_SECRET_CONFIG: str = Field(default="", env="MY_SECRET_CONFIG")


settings = Settings()
