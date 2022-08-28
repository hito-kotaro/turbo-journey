import os
from dotenv import load_dotenv
import requests

load_dotenv()

LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_URL = os.getenv("LINE_URL")
TOKEN_DIC = {"Authorization": "Bearer" + " " + LINE_TOKEN}


# 依頼発行
def post_request(subject: str, request_title: str):
    send_dic = {
        "message": f"\n{subject}さん が\n「{request_title}」\nを発行しました! \n HMTを稼ぐチャンスです!",
        "stickerPackageId": 6136,
        "stickerId": 10551387,
    }
    r = requests.post(LINE_URL, headers=TOKEN_DIC, data=send_dic)
    return {"code": r.status_code}


# 依頼完了
def post_complete(subject: str, request_title: str, owner: str):
    send_dic = {
        "message": (
            f"\n{subject}さん が\n「{request_title}」\nを完了しました!\n{owner}さーん、承認してください!!"
        ),
        "stickerPackageId": 6136,
        "stickerId": 10551390,
    }
    r = requests.post(LINE_URL, headers=TOKEN_DIC, data=send_dic)
    return {"code": r.status_code}


# 承認完了
def post_approve(subject: str, request_title: str):
    send_dic = {
        "message": f"\n{subject}さん が\n「{request_title}」\nを承認しました!\n",
        "stickerPackageId": 6325,
        "stickerId": 10979913,
    }
    r = requests.post(LINE_URL, headers=TOKEN_DIC, data=send_dic)
    return {"code": r.status_code}
