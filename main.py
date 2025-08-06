import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

# Scraper imports
from onexbet_scraper import get_1xbet_live_odds, get_1xbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# Send Telegram alert
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
        print(f"[Telegram] Error: {e}")


# Calculate arbitrage profit %
def calculate_profit(odds_a, odds_b):
    try:
        inv_a = 1 / float(odds_a)
        inv_b = 1 / float(odds_b)
        arb_percent = (inv_a + inv_b) * 100
        profit = round((1 - (inv_a + inv_b)) * 100, 2)
        return profit
    except:
        return -100


# Main bot loop
def run_bot():
    try:
        # Collect all bookmaker odds
        bookmakers_data = (
            get_1xbet_live_odds() + get_1xbet_prematch_odds() +
            get_bcgame_live_odds() + get_bcgame_prematch_odds() +
            get_stake_live_odds() + get_stake_prematch_odds() +
            get_mostbet_live_odds() + get_mostbet_prematch_odds()
        )

        alerts_sent = 0

        # Compare matches
        for i, match_a in enumerate(bookmakers_data):
            for match_b in bookmakers_data[i + 1:]:
                if match_a["match"] == match_b["match"] and match_a["market"] == match_b["market"]:
                    for team in match_a["odds"]:
                        if team in match_b["odds"]:
                            profit = calculate_profit(match_a["odds"][team], match_b["odds"][team])
                            if profit >= 10:  # Only 10%+ profit
                                match_type = "🟢 Live" if match_a["is_live"] else "🔵 Prematch"
                                time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                message = (
                                    f"{match_type} Arbitrage Found\n"
                                    f"{match_a['bookmaker']}: {match_a['odds'][team]}\n"
                                    f"{match_b['bookmaker']}: {match_b['odds'][team]}\n"
                                    f"💰 Profit: {profit}%\n"
                                    f"🕒 {time_now}"
                                )
                                send_telegram_alert(message)
                                alerts_sent += 1
                                if alerts_sent >= 8:
                                    return
    except Exception as e:
        print(f"[Bot Error] {e}")


if __name__ == "__main__":
    print("Bot started. Checking every 5 minutes...")
    while True:
        run_bot()
        time.sleep(300)  # wait 5 minutes
