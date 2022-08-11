from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from db.models import Approve, Bank, Request, User


# 承認依頼一覧を取得する。
def get_approves_query(db: Session):
    statement = """
    SELECT
        a.id,
        a.status,
        r.title,
        r.description,
        r.owner_id,
        r.order_id,
        r.reward,
        a.applicant_id,
        u.name as applicant,
        u2.name as owner
    FROM
        approves as a
    JOIN requests as r
        ON a.request_id = r.id
    JOIN users as u
        ON a.applicant_id = u.id
    JOIN users as u2
        ON r.owner_id = u2.id;
    """
    sql_statement = text(statement)
    result = db.execute(sql_statement)

    approves = []
    for r in result:
        a = {
            "id": r["id"],
            "status": r["status"],
            "title": r["title"],
            "description": r["description"],
            "owner_id": r["owner_id"],
            "owner": r["owner"],
            "order_id": r["order_id"],
            "reward": r["reward"],
            "applicant_id": r["applicant_id"],
            "applicant": r["applicant"],
        }
        # print(a)
        approves.append(a)
    return {"approves": approves}


def update_approve_query(db: Session, new_status: str, approve_id: int):
    approve = db.query(Approve).filter(Approve.id == approve_id).first()
    approve.status = new_status

    bank_id = 1
    # Bankを取得
    bank = db.query(Bank).filter(Bank.id == bank_id).first()

    # rewardを取得
    request = db.query(Request).filter(Request.id == approve.request_id).first()
    # # # 対象のゆーざーを取得
    user = db.query(User).filter(User.id == approve.applicant_id).first()

    reward = request.reward
    tax = bank.gas * request.reward

    # print(bank.gas)
    # print(request.reward)
    # print((request.reward) - (bank.gas * request.reward))
    total = reward - tax
    # print(total)
    user.hmt += total
    bank.hmt += tax

    db.commit()
    return {"message": "update ok"}
