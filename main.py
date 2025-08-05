# Trigger auto-deploy on Render
import os
import time
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_alert(f"🤖 Bot is active\n🕒 Time: {now}")
    time.sleep(60)  # हर 1 मिनट में मैसेज भेजेगा (जैसे कि update check)
