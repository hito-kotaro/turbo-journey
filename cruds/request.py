from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models import Approve, Bank, Request, User
import schema.request_schema as r


def get_requests(db: Session, user_id: int):

    statement = """
    SELECT
        r.id,
        r.title,
        r.description,
        r.owner_id,
        r.order_id,
        r.reward,
        r.public,
        r.status,
        r.created_at,
        r.updated_at,
        CASE WHEN r.is_bank = True THEN b.name ELSE u.name  END AS owner
        FROM requests as r
        LEFT JOIN banks as b
            ON r.owner_id = b.id
        LEFT JOIN users as u
            ON r.owner_id = u.id;
    """
    sql_statement = text(statement)
    results = db.execute(sql_statement)

    # requests = (
    #     db.query(
    #         Request.id,
    #         Request.title,
    #         Request.description,
    #         Request.owner_id,
    #         User.owner
    #         Request.order_id,
    #         Request.reward,
    #         Request.public,
    #         Request.status,
    #         Request.created_at,
    #         Request.updated_at,
    #     )
    #     .filter(
    #         Request.owner_id == User.id,
    #     )
    #     .all()
    # )

    requests = []

    for result in results:
        request = {
            "id": result["id"],
            "title": result["title"],
            "description": result["description"],
            "owner_id": result["owner_id"],
            "owner": result["owner"],
            "order_id": result["order_id"],
            "reward": result["reward"],
            "public": result["public"],
            "status": result["status"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
        requests.append(request)
    print(requests)
    return {"requests": requests}


def complete_request_query(db: Session, request_id: int, user_id: int):
    # print("ok")
    aprove = Approve(applicant_id=user_id, request_id=request_id, status="open")
    request = db.query(Request).filter(Request.id == request_id).first()
    if request.is_bank == False:
        request.status = False

    db.add(aprove)
    db.add(request)
    db.commit()


def create_request_query(db: Session, request: r.RequestCreate, owner_id: int):
    # 発行者を取得
    if request.is_bank:
        user = db.query(Bank).filter(Bank.id == owner_id).first()
    else:
        user = db.query(User).filter(User.id == owner_id).first()
        user.hmt -= request.reward

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
        is_bank=request.is_bank,
        status=True,
    )

    # print(new_request)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request.id


def update_close_request_query(db: Session, request_id: int):
    request = db.query(Request).filter(Request.id == request_id).first()
    request.status == False

    db.commit()
    return {"message": "close ok"}
