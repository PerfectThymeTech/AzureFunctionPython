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
        access_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1NDYzMDA4MDAsImlhdCI6MTU0NjMwMDgwMCwiZXhwIjo0MTAyNDQ0ODAwLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLXBwZS5uZXQvYWIxZjcwOGQtNTBmNi00MDRjLWEwMDYtZDcxYjJhYzdhNjA2LyIsImF1ZCI6Imh0dHBzOi8vc3RvcmFnZS5henVyZS5jb20iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24ifQ.T25N40w8OgfdzV8tJEtX0hZ3udzYKGEMp8RterG_FWjEXQHQ8B919GhSY_2j2yust5CewlOABlcrsq9ZEsbbA0_DqLd_u_MhP8LJHlIAT-Qgblc62h4w6GzND8hoXHYpXw_sH0v1gl7XFiWe4-1fgBC5vcuObDS-ATQGhrB4Ppc9DCa0147YQOOrkTsNjBXZc_n_3qMPcaq-vlfdW1G0WiqUr6qVpw0UQ_-qbmv8IfqIcN16VnIgfk5M3FhV7nmPZxPPlDrz67jioVUoPnIVoxCbD6BUhJ0LAhQiAHi-c_8agWdEBClmGMqgpHGjBjGvhYGBaE-NP9j53b7t5YVgoA"
    )
