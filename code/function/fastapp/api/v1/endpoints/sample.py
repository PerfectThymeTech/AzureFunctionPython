from typing import Annotated

import httpx
from fastapi import APIRouter, Header
from models.sample import SampleRequest, SampleResponse
from utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.post("/sample", response_model=SampleResponse, name="sample")
async def post_predict(
    data: SampleRequest, x_forwarded_for: Annotated[str, Header()] = ""
) -> SampleResponse:
    logger.info(f"Received request: {data}")
    logger.info(f"IP of sender: {x_forwarded_for}")

    # Sample request
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.bing.com")
    logger.info(f"Received response status code: {response.status_code}")

    return SampleResponse(output=f"Hello {data.input}")
