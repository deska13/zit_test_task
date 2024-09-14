from pydantic import BaseModel


class HTTPErrorModel(BaseModel):
    detail: str
