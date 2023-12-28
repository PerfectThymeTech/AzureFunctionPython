from typing import Annotated

import httpx
from fastapi import APIRouter, Header
from fastapp.models.sample import SampleRequest, SampleResponse
from fastapp.utils import setup_logging, setup_tracer
from opentelemetry.trace import SpanKind

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
        "dependency_span", attributes=tracer_attributes, kind=SpanKind.CLIENT
    ) as span:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://www.bing.com")
            logger.info(f"Received response status code: {response.status_code}")
        except Exception as ex:
            span.set_attribute("status", "exception")
            span.record_exception(ex)

    return SampleResponse(output=f"Hello {data.input}")
