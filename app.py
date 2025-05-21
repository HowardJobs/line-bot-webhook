from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")

@app.route('/')
def home():
    return 'LINE Webhook is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    # 立即回應 LINE，避免 timeout
    try:
        events = request.json.get("events", [])
        for event in events:
            if event["type"] == "message":
                source = event.get("source", {})
                if source.get("type") == "group":
                    group_id = source.get("groupId")
                    print(f"✅ 收到群組訊息，groupId：{group_id}")

                    # 傳送訊息到群組
                    headers = {
                        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "to": group_id,
                        "messages": [{
                            "type": "text",
                            "text": f"✅ Bot 收到你的訊息囉！這是群組 ID：{group_id}"
                        }]
                    }
                    requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
    except Exception as e:
        print("⚠️ webhook error:", str(e))

    # 無論如何都立刻回應 LINE 200 OK
    return jsonify({ "status": "ok" })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

