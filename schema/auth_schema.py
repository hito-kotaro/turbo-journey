from xmlrpc.client import boolean
from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    name: str
    password: str
    is_bank: boolean


class AuthResponse(BaseModel):
    access_token: str = Field(None, example="eyjasdjsadkjsahdisabbXXXXXXXXXX")
    token_type: str = Field(None, example="bearer")
    id: int = Field(None, example=1)
    name: str = Field(None, example="tohi")
    is_bank: boolean
