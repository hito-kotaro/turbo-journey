from sqlalchemy.orm import Session
from sqlalchemy.sql import text


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
        print(a)
        approves.append(a)
    return {"approves": approves}
