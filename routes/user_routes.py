from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import schema.user_schema as u
from routes import router_base as rb
from cruds.user import (
    user_exist_check,
    create_user_query,
)


router = rb.create_router("user")


@router.post("/create")
def create_user_api(
    create_user: u.UserCreate,
    db: Session = Depends(rb.get_db),
):
    exist = user_exist_check(db=db, name=create_user.name)
    if exist:
        raise HTTPException(status_code=400, detail="user already exist")

    return create_user_query(db=db, user=create_user)
