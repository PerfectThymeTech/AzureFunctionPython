from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapp.api.v1.api_v1 import api_v1_router
from fastapp.core.config import settings
from fastapp.utils import setup_opentelemetry


def get_app(lifespan) -> FastAPI:
    """Setup the Fast API server.

    RETURNS (FastAPI): The FastAPI object to start the server.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="",
        version=settings.APP_VERSION,
        openapi_url="/openapi.json",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Gracefully start the application before the server reports readiness."""
    setup_opentelemetry(app=app)
    yield
    pass


app = get_app(lifespan=lifespan)
