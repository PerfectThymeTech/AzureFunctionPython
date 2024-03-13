from fastapi import APIRouter
from api.aad.endpoints import token, openid

aad_router = APIRouter()
aad_router.include_router(token.router, prefix="/oauth2/v2.0", tags=["sample"])
aad_router.include_router(openid.router, prefix="/v2.0/.well-known", tags=["sample"])
