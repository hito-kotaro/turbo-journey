from datetime import datetime as dt
from sqlalchemy.orm import Session
from db.models import User
from utils.hash import Hash
from cruds.auth import password_check
import schema.user_schema as u


def user_exist_check(db: Session, name: str):
    user = db.query(User).filter(User.name == name).first()

    return user


def create_user_query(db: Session, user: u.UserCreate):
    hashed_password = Hash.get_password_hash(user.password)
    # ユーザー作成時に経済圏に+10hmtされる
    user = User(
        name=user.name,
        hashed_password=hashed_password,
        hmt=10,
        created_at=dt.now(),
        updated_at=dt.now(),
    )

    db.add(user)
    db.commit()
    return user


def get_user_list(db: Session):
    users = db.query(User).all()

    return {"users": users}


def update_user_name_query(db: Session, user_id: int, new_name: str):
    user = db.query(User).filter(User.id == user_id).first()
    user.name = new_name
    user.updated_at = dt.now()
    db.commit()
    return {"message": "update ok"}


def update_user_pwd_query(db: Session, user_id: int, update_pwd: u.UpdateUserPwd):
    # print(user_id)
    # 新しいパスワードをハッシュ化
    hashed_password = Hash.get_password_hash(update_pwd.new_pwd)

    # 対象ユーザーの取得
    user = db.query(User).filter(User.id == user_id).first()

    # 既存パスワードの検証
    password_check(
        request_password=update_pwd.current_pwd, hashed_password=user.hashed_password
    )

    # パスワードチェックを通過したら新しいパスワードに更新
    user.hashed_password = hashed_password
    user.updated_at = dt.now()

    db.commit()
