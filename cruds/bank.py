from sqlalchemy.orm import Session
from db.models import Bank
from utils.hash import Hash
import schema.bank_schema as b


def bank_exist_check(db: Session, name: str):
    bank = db.query(Bank).filter(Bank.name == name).first()

    return bank


def create_bank_query(db: Session, bank: b.BankCreate):
    hashed_password = Hash.get_password_hash(bank.password)

    bank = Bank(name=bank.name, hashed_password=hashed_password, hmt=1000.00, gas=0.05)

    db.add(bank)
    db.commit()
    return bank


def get_gas_query(db: Session):
    bank = db.query(Bank).filter(Bank.id == 1).first()

    return bank.gas
