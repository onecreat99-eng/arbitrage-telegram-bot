import os
import requests
from bcgame_scraper import get_bcgame_odds  # yaha tumhara scrape function ka naam dalna
from datetime import datetime

# Telegram credentials from GitHub Secrets
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    try:
        data = get_bcgame_odds()  # Tumhara BC.Game scraper ka data yaha milega
        if not data:
            send_telegram_message("⚠ BC.Game se koi data nahi mila.")
        else:
            msg = f"✅ BC.Game Scraper Test {datetime.now().strftime('%H:%M:%S')}\n\n"
            for match in data[:5]:  # sirf pehle 5 match bhejne ke liye
                msg += f"{match['match']} | {match['market']} | Odds: {match['odds']}\n"
            send_telegram_message(msg)
    except Exception as e:
        send_telegram_message(f"❌ BC.Game scraper error: {e}")
