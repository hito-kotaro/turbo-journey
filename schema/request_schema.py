from pydantic import BaseModel


class RequestCreate(BaseModel):
    title: str
    description: str
    order_id: int
    reward: float
    public: bool
