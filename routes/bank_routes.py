from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from cruds.auth import get_current_user
import schema.bank_schema as b
from routes import router_base as rb
from cruds.bank import (
    bank_exist_check,
    create_bank_query,
    get_gas_query,
)

router = rb.create_router("bank")


@router.get("/")
def get_bank_api(
    db: Session = Depends(rb.get_db), current_user: str = Depends(get_current_user)
):
    print(current_user.name)
    bank = {"id": current_user.id, "name": current_user.name, "hmt": current_user.hmt}
    print(bank)
    return bank
    # return get_bank_query(db=db, id=current_user.id)


@router.get("/gas")
def get_gas_api(db: Session = Depends(rb.get_db)):
    return get_gas_query(db=db)


@router.post("/create")
def create_bank_api(
    create_bank: b.BankCreate,
    db: Session = Depends(rb.get_db),
):
    exist = bank_exist_check(db=db, name=create_bank.name)
    if exist:
        raise HTTPException(status_code=400, detail="bank already exist")

    return create_bank_query(db=db, bank=create_bank)
