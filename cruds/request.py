from sqlalchemy import or_
from sqlalchemy.orm import Session
from db.models import Request
import schema.request_schema as r


# Publicの依頼とorder_idが一致する依頼のみ取得
def get_enable_requests(db: Session, user_id: int):
    requests = (
        db.query(Request)
        .filter(or_(Request.public == True, Request.order_id == user_id))
        .all()
    )

    print(requests)
    return {"requests": requests}


def create_request_query(db: Session, request: r.RequestCreate, owner_id: int):

    if request.order_id == -1:
        order_id = None
    else:
        order_id = request.order_id

    new_request = Request(
        title=request.title,
        description=request.description,
        owner_id=owner_id,
        order_id=order_id,
        reward=request.reward,
        public=request.public,
        status=True,
    )

    print(new_request)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request.id
