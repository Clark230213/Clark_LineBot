from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json
import requests
import os

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

api_key = os.environ.get('API_KEY')
line_channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
line_channel_secret = os.environ.get('LINE_CHANNEL_SECRET')

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}
chat_history = []
MAX_HISTORY_LENGTH = 20  # 設定 chat_history 最大長度

@app.route("/callback", methods=['GET', 'POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = line_channel_access_token
        secret = line_channel_secret
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            reply = msg
            chat_history.append({"role": "user", "content": msg})
            data = {
                "model": "gpt-3.5-turbo",
                "messages": chat_history
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']
            print(content)
            reply = content
            # 判斷 chat_history 長度是否超過最大值，若是，刪除最早的一筆資料
            if len(chat_history) >= MAX_HISTORY_LENGTH:
                chat_history.pop(0)
            chat_history.append({"role": "assistant", "content": content})


        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息

    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'  



@app.route('/')
def hello_world():
    return 'Hello, World!' 