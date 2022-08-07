from sqlalchemy.orm import Session
from db.models import Approve, Request, User
import schema.request_schema as r


# Publicの依頼とorder_idが一致する依頼のみ取得
def get_requests(db: Session, user_id: int):
    requests = (
        db.query(
            Request.id,
            Request.title,
            Request.description,
            Request.owner_id,
            User.name.label("owner"),
            Request.order_id,
            Request.reward,
            Request.public,
            Request.status,
            Request.created_at,
            Request.updated_at,
        )
        .filter(
            Request.owner_id == User.id,
        )
        .all()
    )

    return {"requests": requests}


def complete_request_query(db: Session, request_id: int, user_id: int):
    print("ok")
    aprove = Approve(applicant_id=user_id, request_id=request_id, status="open")
    request = db.query(Request).filter(Request.id == request_id).first()
    request.status = False

    db.add(aprove)
    db.add(request)
    db.commit()


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
