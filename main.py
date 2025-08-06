import os
import requests
from datetime import datetime
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("[Telegram] Missing BOT_TOKEN or CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[Telegram] Error: {e}")

def calculate_profit(odds_a, odds_b):
    try:
        inv_a = 1 / float(odds_a)
        inv_b = 1 / float(odds_b)
        return round((1 - (inv_a + inv_b)) * 100, 2)
    except:
        return -100

def run_bot():
    try:
        data = (
            get_bcgame_live_odds() +
            get_bcgame_prematch_odds() +
            get_mostbet_live_odds() +
            get_mostbet_prematch_odds()
        )

        if not data:
            print("[Bot] No data fetched from scrapers.")
            return

        for i, match_a in enumerate(data):
            for match_b in data[i + 1:]:
                if match_a["match"] == match_b["match"] and match_a["market"] == match_b["market"]:
                    for team in match_a["odds"]:
                        if team in match_b["odds"]:
                            # Test mode: no profit filter
                            profit = calculate_profit(match_a["odds"][team], match_b["odds"][team])
                            match_type = "🟢 Live" if match_a["is_live"] else "🔵 Prematch"
                            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            message = (
                                f"{match_type} Arbitrage (TEST MODE)\n"
                                f"⚫ {match_a['bookmaker']}: {match_a['odds'][team]}\n"
                                f"⚫ {match_b['bookmaker']}: {match_b['odds'][team]}\n"
                                f"💰 Profit: {profit}%\n"
                                f"🕒 {time_now}"
                            )
                            send_telegram_alert(message)
    except Exception as e:
        print(f"[Bot Error] {e}")

if __name__ == "__main__":
    run_bot()
