from fastapi import Depends
from sqlalchemy.orm import Session
from routes import router_base as rb
import schema.approve_schema as a
from cruds.approve import get_approves_query
from cruds.auth import get_current_user

router = rb.create_router("approve")


@router.get("/", response_model=a.Approves)
def get_request_api(
    db: Session = Depends(rb.get_db),
    current_user: str = Depends(get_current_user),
):

    return get_approves_query(db=db)
