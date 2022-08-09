from typing import List
from pydantic import BaseModel


class Approve(BaseModel):
    id: int
    status: str
    title: str
    description: str
    reward: float
    applicant: str

    class Config:
        orm_mode = True


class Approves(BaseModel):
    approves: List[Approve]

    class Config:
        orm_mode = True
