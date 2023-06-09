import azure.functions as func
from fastapi import FastAPI
from function.api.v1.api_v1 import api_v1_router
from function.core.config import settings


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        openapi_url="/openapi.json",
        debug=settings.DEBUG,
    )
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    return app


fastapi_app = get_app()


@fastapi_app.on_event("startup")
async def startup_event():
    pass


@fastapi_app.on_event("shutdown")
async def shutdown_event():
    pass


app = func.AsgiFunctionApp(
    app=fastapi_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
