from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import schema.bank_schema as b
from routes import router_base as rb
from cruds.bank import (
    bank_exist_check,
    create_bank_query,
)

router = rb.create_router("bank")


@router.post("/create")
def create_bank_api(
    create_bank: b.BankCreate,
    db: Session = Depends(rb.get_db),
):
    exist = bank_exist_check(db=db, name=create_bank.name)
    if exist:
        raise HTTPException(status_code=400, detail="bank already exist")

    return create_bank_query(db=db, bank=create_bank)
