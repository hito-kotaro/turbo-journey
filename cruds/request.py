from sqlalchemy.orm import Session
from db.models import Request
import schema.request_schema as r


def create_request_query(db: Session, request: r.RequestCreate, owner_id: int):

    new_request = Request(
        title=request.title,
        description=request.description,
        owner_id=owner_id,
        order_id=request.order_id,
        reward=request.reward,
        public=request.public,
    )

    print(new_request)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request.id
