from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import schema.user_schema as u
from routes import router_base as rb
from cruds.auth import get_current_user
from cruds.user import (
    user_exist_check,
    create_user_query,
)


router = rb.create_router("user")


@router.get("/")
def get_user_api(
    db: Session = Depends(rb.get_db),
    current_user: str = Depends(get_current_user),
):
    test = {"id": current_user.id, "name": current_user.name, "hmt": current_user.hmt}
    print(test)
    return test


@router.post("/create")
def create_user_api(
    create_user: u.UserCreate,
    db: Session = Depends(rb.get_db),
):
    exist = user_exist_check(db=db, name=create_user.name)
    if exist:
        raise HTTPException(status_code=400, detail="user already exist")

    return create_user_query(db=db, user=create_user)
