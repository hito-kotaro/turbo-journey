from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import schema.user_schema as u
from routes import router_base as rb
from cruds.auth import get_current_user
from cruds.user import (
    get_user_list,
    update_user_pwd_query,
    user_exist_check,
    create_user_query,
    update_user_name_query,
)


router = rb.create_router("user")


@router.get("/")
def get_user_api(
    db: Session = Depends(rb.get_db),
    current_user: str = Depends(get_current_user),
):
    user = {"id": current_user.id, "name": current_user.name, "hmt": current_user.hmt}
    return user


@router.get("/all", response_model=u.Users)
def get_user_list_api(
    db: Session = Depends(rb.get_db),
    current_user: str = Depends(get_current_user),
):
    return get_user_list(db=db)


@router.post("/create")
def create_user_api(
    create_user: u.UserCreate,
    db: Session = Depends(rb.get_db),
):
    exist = user_exist_check(db=db, name=create_user.name)
    if exist:
        raise HTTPException(status_code=400, detail="user already exist")

    return create_user_query(db=db, user=create_user)


@router.put("/update/name")
def update_user_name_api(
    update_name: u.UpdateUserName,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(rb.get_db),
):
    exist = user_exist_check(db=db, name=update_name.name)
    if exist:
        raise HTTPException(status_code=400, detail="user already exist")
    return update_user_name_query(
        db=db, user_id=current_user.id, new_name=update_name.name
    )


@router.put("/update/pwd")
def update_user_pwd_api(
    update_pwd: u.UpdateUserPwd,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(rb.get_db),
):
    return update_user_pwd_query(db=db, user_id=current_user.id, update_pwd=update_pwd)
