# main.py
import time
import threading
from flask import Flask
from onexbet import get_1xbet_live_odds, get_1xbet_prematch_odds
from stake import get_stake_live_odds, get_stake_prematch_odds
from bcgame import get_bcgame_live_odds, get_bcgame_prematch_odds

# Telegram settings
import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_arbitrage():
    print(f"[{datetime.now()}] Checking arbitrage...")
    try:
        odds_data = []
        odds_data.extend(get_1xbet_live_odds())
        odds_data.extend(get_1xbet_prematch_odds())
        odds_data.extend(get_stake_live_odds())
        odds_data.extend(get_stake_prematch_odds())
        odds_data.extend(get_bcgame_live_odds())
        odds_data.extend(get_bcgame_prematch_odds())

        # यहां arbitrage detection logic डाल सकते हैं
        if odds_data:
            send_telegram_message(f"✅ Odds collected: {len(odds_data)}")
        else:
            send_telegram_message("⚠ No odds found.")

    except Exception as e:
        print(f"Arbitrage Error: {e}")
        send_telegram_message(f"❌ Error: {e}")

def run_scheduler():
    while True:
        check_arbitrage()
        time.sleep(300)  # हर 5 मिनट में run

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
