import base64
from hashlib import sha256
from typing import Annotated

from fastapi import Header, HTTPException
from fastapp.core.config import settings


async def verify_health_auth_header(
    x_ms_auth_internal_token: Annotated[str, Header()]
) -> bool:
    """Returns true if SHA256 of header_value matches WEBSITE_AUTH_ENCRYPTION_KEY.
    Documentation: https://learn.microsoft.com/en-us/azure/app-service/monitor-instances-health-check?tabs=python#authentication-and-security

    x_ms_auth_internal_token: Value of the x-ms-auth-internal-token header.
    RETURNS (bool): Specifies whether the header matches.
    """
    website_auth_encryption_key = settings.WEBSITE_AUTH_ENCRYPTION_KEY
    hash = base64.b64encode(
        sha256(website_auth_encryption_key.encode("utf-8")).digest()
    ).decode("utf-8")
    if hash != x_ms_auth_internal_token:
        raise HTTPException(
            status_code=400, detail="x-ms-auth-internal-token is invalid"
        )
    else:
        return True
