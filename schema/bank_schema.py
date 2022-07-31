from pydantic import BaseModel


class BankCreate(BaseModel):
    name: str
    password: str
