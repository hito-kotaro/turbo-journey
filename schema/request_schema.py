from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Request(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    owner: str
    order_id: Optional[int]
    reward: int
    public: bool
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Requests(BaseModel):
    requests: List[Request]

    class Config:
        orm_mode = True


class RequestCreate(BaseModel):
    title: str
    description: str
    order_id: int
    reward: float
    public: bool
    is_bank: bool


class RequestClose(BaseModel):
    id: int
