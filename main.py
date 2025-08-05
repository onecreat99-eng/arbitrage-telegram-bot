import os
import requests

# ✅ Securely fetch values from environment
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(response.text)

# ✅ Test message
send_telegram_message("✅ Bot is working and connected to Telegram")
