from fastapi import Depends
from sqlalchemy.orm import Session
import schema.request_schema as r
from routes import router_base as rb
from cruds.request import create_request_query, get_enable_requests
from cruds.auth import get_current_user

router = rb.create_router("request")


@router.get("/", response_model=r.Requests)
def get_request_api(
    db: Session = Depends(rb.get_db),
    current_user: str = Depends(get_current_user),
):

    return get_enable_requests(db=db, user_id=current_user.id)


@router.post("/create")
def create_request_api(
    create_request: r.RequestCreate,
    db: Session = Depends(rb.get_db),
    current_user: str = Depends(get_current_user),
):
    return create_request_query(db=db, request=create_request, owner_id=current_user.id)