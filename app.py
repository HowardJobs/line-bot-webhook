from flask import Flask, request
import requests

app = Flask(__name__)

import os
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")

@app.route('/')
def home():
    return 'LINE Webhook is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    print("🔔 收到 LINE 訊息：", payload)

    # 從事件中取得群組 ID
    if 'events' in payload:
        for event in payload['events']:
            source = event.get('source', {})
            if source.get('type') == 'group':
                group_id = source.get('groupId')
                print(f"✅ 取得群組 ID：{group_id}")

                # 傳送確認訊息到該群組
                reply_message = {
                    "to": group_id,
                    "messages": [{
                        "type": "text",
                        "text": f"✅ Bot 收到你的訊息囉！這是群組 ID：{group_id}"
                    }]
                }
                headers = {
                    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                requests.post('https://api.line.me/v2/bot/message/push',
                              headers=headers, json=reply_message)
    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)
