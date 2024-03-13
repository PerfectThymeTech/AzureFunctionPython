from pydantic import BaseModel


class TokenRequest(BaseModel):
    input: str


class TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    ext_expires_in: int
    access_token: str = "eyJhbGciOiJSUzI1NiIsInR5cC....eyJuYmYiOjE1NDYzMDA4MDAsImlhdCI6MT..."
