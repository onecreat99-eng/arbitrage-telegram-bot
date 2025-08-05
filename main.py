import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(response.text)

# ✅ Test message
send_telegram_message("✅ Bot is working and connected to Telegram!")
