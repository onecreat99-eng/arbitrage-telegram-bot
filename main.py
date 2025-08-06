# Trigger auto-deploy on Render
import os
import time
import requests
from dotenv import load_dotenv
from oddspedia import get_oddspedia_odds
from oddsam import get_oddsam_odds
from utils import calculate_profit, normalize_team_name
from datetime import datetime

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram send error: {e}")

def run_bot():
    try:
        oddspedia_data = get_oddspedia_odds()
        oddsam_data = get_oddsam_odds()
        alerts_sent = 0

        for match_a in oddspedia_data:
            for match_b in oddsam_data:
                if normalize_team_name(match_a["match"]) == normalize_team_name(match_b["match"]):
                    for team in match_a["odds"]:
                        if team in match_b["odds"]:
                            profit = calculate_profit(match_a["odds"][team], match_b["odds"][team])
                            if profit >= 10:  # 10% profit filter
                                match_type = "🟢 Live" if match_a["type"].lower() == "live" else "🔵 Prematch"
                                time_now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                                message = (
                                    f"{match_type} Arbitrage Found!\n"
                                    f"{match_a['bookmaker']}: {match_a['odds'][team]}  vs  "
                                    f"{match_b['bookmaker']}: {match_b['odds'][team]}\n"
                                    f"💰 Profit: {profit}%\n"
                                    f"⏰ {time_now}"
                                )
                                send_telegram_alert(message)
                                alerts_sent += 1
                                if alerts_sent >= 8:
                                    return
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    print("Bot started. Checking every 5 minutes...")
    while True:
        run_bot()
        time.sleep(300)  # wait 5 minutes
