import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    r = requests.post(url, json=payload)
    print(r.json())

send_telegram_message("✅ Secure Telegram test message from GitHub Actions.")
