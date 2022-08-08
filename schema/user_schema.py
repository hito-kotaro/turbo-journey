from typing import List
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    password: str


class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Users(BaseModel):
    users: List[User]

    class Config:
        orm_mode = True
