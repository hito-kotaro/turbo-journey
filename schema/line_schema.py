from pydantic import BaseModel


class ResponseCode(BaseModel):
    code: int


class PostRequestTitle(BaseModel):
    request_title: str


class PostComplete(PostRequestTitle):
    owner: str
