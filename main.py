import os
import telegram
from dotenv import load_dotenv
import time

# ✅ Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

while True:
    message = "✅ Bot is working! Arbitrage alert will be added here."
    bot.send_message(chat_id=CHAT_ID, text=message)
    time.sleep(3600)  # Sends message every hour (for demo)
import os
import requests
from dotenv import load_dotenv

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

# 🟢 Test message
send_telegram_message("✅ Bot is working and connected to Telegram!")
