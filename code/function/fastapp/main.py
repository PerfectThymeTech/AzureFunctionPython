from fastapi import FastAPI
from fastapp.api.v1.api_v1 import api_v1_router
from fastapp.core.config import settings
from fastapp.utils import setup_tracer


def get_app() -> FastAPI:
    """Setup the Fast API server.

    RETURNS (FastAPI): The FastAPI object to start the server.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        openapi_url="/openapi.json",
        debug=settings.DEBUG,
    )
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    return app


app = get_app()


@app.on_event("startup")
async def startup_event():
    """Gracefully start the application before the server reports readiness."""
    setup_tracer(app=app)


@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully close connections before shutdown of the server."""
    pass
