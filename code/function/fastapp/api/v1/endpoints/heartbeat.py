from typing import Any

from fastapi import APIRouter, Depends
from health.validate_request import verify_health_auth_header
from models.heartbeat import HearbeatResult
from utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.get(
    "/heartbeat",
    response_model=HearbeatResult,
    name="heartbeat",
    dependencies=[Depends(verify_health_auth_header)],
)
async def get_hearbeat() -> Any:
    logger.info("Received Heartbeat Request")
    return HearbeatResult(isAlive=True)
