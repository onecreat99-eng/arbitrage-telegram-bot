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

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram Arbitrage Bot is running!"

def send_alerts():
    global alerts_sent_today, today_date

    while True:
        now = datetime.utcnow()

        # Reset alert count at midnight
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

        time.sleep(3600)

# Start alerts in background
threading.Thread(target=send_alerts).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
