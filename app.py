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
                    # 🔕 不發任何訊息回群組，只記錄 groupId
    except Exception as e:
        print("⚠️ webhook error:", str(e))

    # 無論如何都立刻回應 LINE 200 OK
    return jsonify({ "status": "ok" })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
