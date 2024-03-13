from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Form
from models.openid import OpenIdRequest, OpenIdResponse
from utils import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.get("/openid-configuration", response_model=OpenIdResponse, name="token")
async def post_predict(
) -> OpenIdResponse:
    tenant_id = "mytenantid"

    return OpenIdResponse(
        authorization_endpoint=f"https://127.0.0.1:8000/{tenant_id}/oauth2/v2.0/authorize",
        token_endpoint=f"https://127.0.0.1:8000/{tenant_id}/oauth2/v2.0/token",
        token_endpoint_auth_methods_supported=[
            "client_secret_post",
            "private_key_jwt"
        ],
        jwks_uri=f"https://127.0.0.1:8000/{tenant_id}/discovery/v2.0/keys",
        userinfo_endpoint="https://graph.microsoft.com/oidc/userinfo",
        subject_types_supported=[
            "pairwise"
        ]
    )
