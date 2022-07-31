import os
from sqlalchemy.orm import Session
from db.models import User, Bank
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from routes import router_base as rb
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# アクセストークンの生成
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 存在確認
def exist_check(check):
    if not check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


# パスワードの検証
def password_check(request_password: str, hashed_password: str):
    pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_cxt.verify(request_password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )


# 認証処理
def auth_user(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(rb.get_db)
):
    user = db.query(User).filter(User.name == request.name).first()

    exist_check(check=user)
    password_check(
        request_password=request.password, hashed_password=user.hashed_password
    )

    access_token = create_access_token(data={"id": user.id, "name": user.name})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
        "name": user.name,
        "isBank": False,
    }


def auth_bank(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(rb.get_db)
):
    bank = db.query(Bank).filter(Bank.name == request.name).first()

    exist_check(check=bank)
    password_check(
        request_password=request.password, hashed_password=bank.hashed_password
    )

    access_token = create_access_token(data={"id": bank.id, "name": bank.name})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "bank_id": bank.id,
        "bank_name": bank.name,
        "isBank": True,
    }


def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user.id} not found",
        )

    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(rb.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Colud not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_name: str = payload.get("name")
        user_id: int = payload.get("id")
        if user_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(db=db, id=user_id)
    if user is None:
        raise credentials_exception
    return user
