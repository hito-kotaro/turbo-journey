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
        "message": f"\n{subject}さん が依頼「{request_title}」を発行しました！ \n HMTを稼ぐチャンスです!",
        "stickerPackageId": 6136,
        "stickerId": 10551387,
    }
    r = requests.post(LINE_URL, headers=TOKEN_DIC, data=send_dic)
    return r.status_code


# 依頼完了
def post_complete(subject: str, request_title: str, owner: str):
    send_dic = {
        "message": f"\n{subject}が「{request_title}」を完了しました！\n{owner}さーん、承認してください!!",
        "stickerPackageId": 6136,
        "stickerId": 10551378,
    }
    r = requests.post(LINE_URL, headers=TOKEN_DIC, data=send_dic)
    return r.status_code


# 承認完了
def post_approve(subject: str, request_title: str):
    send_dic = {
        "message": f"\n{subject}が「{request_title}」を承認しました！\n",
        "stickerPackageId": 6325,
        "stickerId": 10979913,
    }
    r = requests.post(LINE_URL, headers=TOKEN_DIC, data=send_dic)
    return r.status_code


def post_message(subject: str, action: str):
    token_dic = {"Authorization": "Bearer" + " " + LINE_TOKEN}
    # actions
    # 0:依頼発行
    # 1:承認依頼発行
    # 2:承認完了
    # action_dic = {"request": ["が依頼を発行しました！", 6136, 10551380]}
    if action == "request":
        send_dic = {
            "message": "\n" + subject + "が依頼を発行しました! \n HANAMARUを稼ぐチャンスです!",
            "stickerPackageId": 6136,
            "stickerId": 10551387,
        }
    elif action == "approve":
        send_dic = {
            "message": "\n" + subject + "が依頼を発行しました! \n HANAMARUを稼ぐチャンスです!",
            "stickerPackageId": 6136,
            "stickerId": 10551387,
        }
    print(token_dic)
    print(send_dic)
    r = requests.post(LINE_URL, headers=token_dic, data=send_dic)
    return r.status_code
