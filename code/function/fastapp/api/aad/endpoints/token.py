from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Form
from models.token import TokenRequest, TokenResponse
from utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.post("/token", response_model=TokenResponse, name="token")
async def post_predict(
    grant_type: Annotated[str, Form()],
    client_id: Annotated[str, Form()],
    scope: Annotated[str, Form()],
    client_secret: Annotated[str, Form()]
) -> TokenResponse:

    return TokenResponse(
        token_type="Bearer",
        expires_in=3599,
        ext_expires_in=3599,
        access_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX...eyJuYmYiOjE1NDYzMDA4MDAsImlhdCI6MTU0NjMwMDgwMCwiZXhwIjo0M..."
    )
