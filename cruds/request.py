from datetime import datetime as dt
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
        r.is_bank,
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
            "is_bank": result["is_bank"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
        requests.append(request)
    print(requests)
    return {"requests": requests}


def complete_request_query(db: Session, request_id: int, user_id: int):
    # print("ok")
    aprove = Approve(
        applicant_id=user_id,
        request_id=request_id,
        status="open",
        created_at=dt.now(),
        updated_at=dt.now(),
    )
    request = db.query(Request).filter(Request.id == request_id).first()
    if request.is_bank == False:
        request.status = False
        request.updated_at = dt.now()

    db.add(aprove)
    db.add(request)
    db.commit()


def create_request_query(db: Session, request: r.RequestCreate, owner_id: int):
    # ??????????????????
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
        created_at=dt.now(),
        updated_at=dt.now(),
    )

    # print(new_request)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request.id


# gas????????????????????????????????????????????????
def sendBackToken(db: Session, user_id: int, reward: float):
    bank = db.query(Bank).filter(Bank.id == 1).first()
    user = db.query(User).filter(User.id).first()

    # gas?????????
    gas = bank.gas

    # reward??????tax?????????
    tax = reward * gas

    # tax???bank?????????
    bank.hmt += tax

    # ?????????user?????????
    user.hmt += reward - tax

    user.updated_at = dt.now()
    bank.updated_at = dt.now()
    db.commit()
    return 0


def update_close_request_query(db: Session, request_id: int, user_id: int):
    request = db.query(Request).filter(Request.id == request_id).first()
    request.status = False
    request.updated_at = dt.now()
    sendBackToken(db=db, user_id=user_id, reward=request.reward)

    db.commit()
    return {"message": "close ok"}
