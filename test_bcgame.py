from bcgame_scraper import get_bcgame_odds
import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    data = get_bcgame_odds()
    if data:
        send_telegram_message(f"✅ BC.Game scraper fetched {len(data)} markets successfully!")
    else:
        send_telegram_message("❌ BC.Game scraper failed or returned no data.")
