from typing import Annotated

import aiohttp
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
    logger.info(f"Received request: {data}")

    # Sample request
    tracer_attributes = {"http.client_ip": x_forwarded_for}
    with tracer.start_as_current_span(
        "dependency_span", attributes=tracer_attributes
    ) as span:
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(url="https://www.bing.com/") as response:
                    resp_status_code = response.status
                    resp_text = await response.text()
            logger.info(f"Received response status code: {resp_status_code}")
        except Exception as ex:
            span.set_attribute("status", "exception")
            span.record_exception(ex)

    return SampleResponse(output=f"Hello {data.input}")
