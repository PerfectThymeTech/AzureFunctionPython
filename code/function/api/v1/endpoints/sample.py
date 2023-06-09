from typing import Any

from fastapi import APIRouter
from function.models.sample import SampleRequest, SampleResponse
from function.utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.post("/create", response_model=SampleResponse, name="create")
async def post_predict(
    data: SampleRequest,
) -> SampleResponse:
    logger.info(f"Received request: {data}")
    return SampleResponse(output=f"Hello ${data.input}")