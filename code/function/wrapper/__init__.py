import azure.functions as func
from fastapp.main import app
from fastapp.utils import setup_tracer
from opentelemetry.context import attach, detach
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = setup_tracer(__name__)


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    # Start distributed tracing
    functions_current_context = {
        "traceparent": context.trace_context.Traceparent,
        "tracestate": context.trace_context.Tracestate,
    }
    parent_context = TraceContextTextMapPropagator().extract(
        carrier=functions_current_context
    )
    token = attach(parent_context)

    # Function logic
    try:
        with tracer.start_as_current_span("wrapper") as span:
            response = await func.AsgiMiddleware(app).handle_async(req, context)
    finally:
        # End distributed tracing
        detach(token)

    return response
