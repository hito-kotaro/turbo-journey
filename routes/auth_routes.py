from fastapi import Depends
from sqlalchemy.orm import Session
import routes.router_base as rb
from schema import auth_schema as a
from passlib.context import CryptContext
from cruds.auth import auth_bank, auth_user

router = rb.create_router("auth")


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=a.AuthResponse)
def create_access_token(request: a.AuthRequest, db: Session = Depends(rb.get_db)):
    print(request)

    if request.isBank:
        return auth_bank(request=request, db=db)
    else:
        return auth_user(request=request, db=db)
