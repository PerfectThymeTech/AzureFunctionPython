from pydantic import BaseModel


class HearbeatResult(BaseModel):
    isAlive: bool
