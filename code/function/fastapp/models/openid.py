from pydantic import BaseModel
from typing import List


class OpenIdRequest(BaseModel):
    input: str


class OpenIdResponse(BaseModel):
    authorization_endpoint: str
    token_endpoint: str
    token_endpoint_auth_methods_supported: List[str]
    jwks_uri: str
    userinfo_endpoint: str
    subject_types_supported: List[str]
