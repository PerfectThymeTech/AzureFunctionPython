from fastapi import APIRouter
from function.api.v1.endpoints import heartbeat, sample

api_v1_router = APIRouter()
api_v1_router.include_router(sample.router, prefix="/landingZone", tags=["sample"])
api_v1_router.include_router(heartbeat.router, prefix="/health", tags=["health"])
