from pydantic import BaseModel


class SampleRequest(BaseModel):
    input: str


class SampleResponse(BaseModel):
    output: str
