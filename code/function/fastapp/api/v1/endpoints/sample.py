from typing import Any

from fastapi import APIRouter
from fastapp.models.sample import SampleRequest, SampleResponse
from fastapp.utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.post("/sample", response_model=SampleResponse, name="sample")
async def post_predict(
    data: SampleRequest,
) -> SampleResponse:
    logger.info(f"Received request: {data}")
    return SampleResponse(output=f"Hello {data.input}")
