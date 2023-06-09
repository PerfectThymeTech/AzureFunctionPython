from typing import Any

from fastapi import APIRouter
from fastapp.models.heartbeat import HearbeatResult
from fastapp.utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.get("/heartbeat", response_model=HearbeatResult, name="heartbeat")
async def get_hearbeat() -> Any:
    logger.info("Received Heartbeat Request")
    return HearbeatResult(isAlive=True)
