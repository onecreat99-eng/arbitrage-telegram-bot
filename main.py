# Trigger auto-deploy on Render
import os
import time
import threading
import requests
from datetime import datetime
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def background_loop():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_alert(f"🤖 Bot चालू है!\n🕒 {now}")
        time.sleep(60)

@app.route('/')
def home():
    return "Bot is running!"

# Threading se background task run karenge
if __name__ == '__main__':
    threading.Thread(target=background_loop).start()
    app.run(host='0.0.0.0', port=10000)
