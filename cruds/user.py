from sqlalchemy.orm import Session
from db.models import User
from utils.hash import Hash
import schema.user_schema as u


def user_exist_check(db: Session, name: str):
    user = db.query(User).filter(User.name == name).first()

    return user


def create_user_query(db: Session, user: u.UserCreate):
    hashed_password = Hash.get_password_hash(user.password)
    # ユーザー作成時に経済圏に+10hmtされる
    user = User(name=user.name, hashed_password=hashed_password, hmt=10)

    db.add(user)
    db.commit()
    return user


def get_user_list(db: Session):
    users = db.query(User).all()

    return {"users": users}
