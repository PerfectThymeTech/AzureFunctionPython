from typing import Annotated

import httpx
from fastapi import APIRouter, Header
from fastapp.models.sample import SampleRequest, SampleResponse
from fastapp.utils import setup_logging, setup_tracer

logger = setup_logging(__name__)
tracer = setup_tracer(__name__)

router = APIRouter()


@router.post("/sample", response_model=SampleResponse, name="sample")
async def post_predict(
    data: SampleRequest, x_forwarded_for: Annotated[str, Header()] = ""
) -> SampleResponse:
    logger.info(f"Received request: '{data}' from ip '{x_forwarded_for}'")

    # Sample request
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.bing.com/")
    logger.info(f"Received response status code: {response.status_code}")

    return SampleResponse(output=f"Hello {data.input}")
