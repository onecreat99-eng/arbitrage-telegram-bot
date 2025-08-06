# Trigger auto-deploy on Render
import requests
import os
from datetime import datetime

# Telegram credentials from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Profit threshold
PROFIT_THRESHOLD = 10.0

# Fetch odds from Oddspedia
def get_oddspedia_odds():
    try:
        url = "https://oddspedia.com/api/v1/getOdds?bookmakers=1xbet,bc.game"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Oddspedia error:", e)
        return None

# Fetch odds from Odds.am
def get_oddsam_odds():
    try:
        url = "https://api.odds.am/v3/offer/surebets"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Odds.am error:", e)
        return None

# Send Telegram alert
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

# Main arbitrage check
def check_arbitrage():
    data_oddspedia = get_oddspedia_odds()
    data_oddsam = get_oddsam_odds()

    opportunities = []

    if data_oddspedia:
        for item in data_oddspedia.get("data", []):
            profit = item.get("profit", 0)
            if profit >= PROFIT_THRESHOLD:
                opportunities.append(f"🟢 <b>{item['sport']}</b>\nProfit: {profit}%\nSource: Oddspedia")

    if data_oddsam:
        for item in data_oddsam.get("data", []):
            profit = item.get("profit", 0)
            if profit >= PROFIT_THRESHOLD:
                opportunities.append(f"🟢 <b>{item['sport']}</b>\nProfit: {profit}%\nSource: Odds.am")

    if opportunities:
        message = "🔥 <b>Arbitrage Opportunities</b> 🔥\n\n" + "\n\n".join(opportunities)
        send_telegram_alert(message)
    else:
        print("No opportunities found.")

if __name__ == "__main__":
    check_arbitrage()
