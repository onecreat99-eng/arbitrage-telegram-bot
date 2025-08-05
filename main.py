# Trigger auto-deploy on Render
import os
import time
import threading
from datetime import datetime
from flask import Flask
from telegram import Bot

# Telegram bot setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Alert limit config
MAX_ALERTS_PER_DAY = 4
alerts_sent_today = 0
today_date = datetime.utcnow().date()

# Flask web app for Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram arbitrage bot running ✅"

def send_alert():
    global alerts_sent_today, today_date

    while True:
        now = datetime.utcnow()

        # Reset daily count at midnight UTC
        if now.date() != today_date:
            today_date = now.date()
            alerts_sent_today = 0

        if alerts_sent_today < MAX_ALERTS_PER_DAY:
            message = (
                "🟢 *LIVE Arbitrage Found!*\n\n"
                "🔅⚫ 1xBet: 2.1\n"
                "🔅⚫ Stake: 2.2\n"
                "💰 Profit: 10.5%\n"
                "⏰ Match: ABC vs XYZ\n"
            )
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
            alerts_sent_today += 1

        time.sleep(3600)  # Wait 1 hour before next alert
