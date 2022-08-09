from sqlalchemy.orm import Session
from db.models import Approve, Request, User


# 承認依頼一覧を取得する。
def get_approves_query(db: Session):
    approves = (
        db.query(
            Approve.id,
            Approve.status,
            Request.title,
            Request.description,
            Request.owner_id,
            Request.order_id,
            Request.reward,
            User.name.label("applicant"),
        )
        .filter(Approve.request_id == Request.id, Approve.applicant_id == User.id)
        .all()
    )

    return {"approves": approves}
