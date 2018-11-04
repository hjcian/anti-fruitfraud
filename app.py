from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('rYeJ0hEeOWbGCUHgkm04LUUz9LkHGKxHFbKl/6qFpLSvcnBwAPwNvGIpkMw2FcOlk4/8fVpAe/yNsPEmysEpDb0wyAxp1M+GCSIcBCZG/lFkPbRsus2JvF454W8hUSbO1nEc9ar8fxfZGQJqknUMaAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('116c10a4943bedf7211cabc85aec1da2')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

    

# main function
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received = event.message.text
    print("received: {}".format(received))
    message = TextSendMessage(text=received)
    print("message obj: {}".format(message))
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
