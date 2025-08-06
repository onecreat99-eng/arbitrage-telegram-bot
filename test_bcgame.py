from bcgame_scraper import get_bcgame_odds
import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("DEBUG: BOT_TOKEN =", BOT_TOKEN)
print("DEBUG: CHAT_ID =", CHAT_ID)

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ ERROR: Telegram bot token or chat ID not found.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, json=payload)
    print("DEBUG: Telegram API response:", r.text)

if __name__ == "__main__":
    try:
        data = get_bcgame_odds()
        send_telegram_message(f"✅ BC.Game scraper ran successfully. Markets found: {len(data)}")
    except Exception as e:
        send_telegram_message(f"❌ BC.Game scraper failed: {e}")
        print("ERROR:", e)
