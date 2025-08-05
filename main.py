# Trigger auto-deploy on Render
import os
from dotenv import load_dotenv
import time
import logging
import requests

# ✅ Logger Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# ✅ Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔍 Debug logs
logging.info("✅ .env file loaded")
logging.info(f"🤖 BOT_TOKEN: {'Found' if BOT_TOKEN else 'Missing'}")
logging.info(f"💬 CHAT_ID: {'Found' if CHAT_ID else 'Missing'}")

# 📤 Telegram Function
def send_telegram_message(message):
    logging.info("📨 Sending message to Telegram...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        logging.info(f"✅ Telegram response: {response.status_code}")
    except Exception as e:
        logging.error(f"❌ Telegram send error: {e}")

# 🚀 Startup message
send_telegram_message("✅ Bot started successfully and is now running...")

# 🔄 Test loop (fake alert every 60 sec)
while True:
    logging.info("🔁 Checking for arbitrage opportunities...")

    fake_alert = "🟢 LIVE Arbitrage Found!\n⚫ 1xBet: 2.1\n⚫ Stake: 2.2\n💰 Profit: 10.5%\n⏰ Match: ABC vs XYZ"
    send_telegram_message(fake_alert)

    logging.info("⏸️ Waiting 60 seconds before next check...")
    time.sleep(60)
