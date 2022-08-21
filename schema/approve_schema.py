from datetime import datetime
from typing import List
from pydantic import BaseModel


class Approve(BaseModel):
    id: int
    status: str
    title: str
    description: str
    owner_id: int
    owner: str
    reward: float
    applicant: str
    applicant_id: int
    description: str
    is_bank: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Approves(BaseModel):
    approves: List[Approve]

    class Config:
        orm_mode = True


class UpdateApprove(BaseModel):
    id: int
    new_status: str
