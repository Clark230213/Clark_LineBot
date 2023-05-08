# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('s47JHrUKfsC1fqVLWzp+OQ8Gj23Vr/rguDmLyeiCYrNaD/JLaxS3DlIAyevsikXaWhFdth0uoPEBTk9ZXPrEMzyj4l7WasiV9LTEY2x1flYRSc0jqkMohRa0gNKFgOBktyHPKjmpRepQTuOpDFlhcQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c68430d99c0fedee7c7b3afe930010ab')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()