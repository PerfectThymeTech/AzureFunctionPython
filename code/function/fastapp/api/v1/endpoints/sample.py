from typing import Any

import aiohttp
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

    # Sample request
    async with aiohttp.ClientSession() as client:
        async with client.get(url="https://www.bing.com/") as response:
            resp_status_code = response.status
    logger.info(f"Received response status code: {resp_status_code}")

    return SampleResponse(output=f"Hello. Dependency Status Code: {resp_status_code}")
