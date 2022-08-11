from pydantic import BaseModel


class BankCreate(BaseModel):
    name: str
    password: str


class GasUpdate(BaseModel):
    new_gas: float
