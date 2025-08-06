import os
import time
from datetime import datetime
from dotenv import load_dotenv

from onexbet_scraper import get_onexbet_live_odds, get_onexbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

import requests

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Daily alert limit
MAX_ALERTS_PER_DAY = 8
alerts_sent_today = 0
current_day = datetime.now().day

def send_telegram_alert(message):
    """Send alert to Telegram bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram send error: {e}")

def calculate_profit(odd_a, odd_b):
    """Calculate arbitrage profit percentage"""
    try:
        inv_sum = (1/odd_a) + (1/odd_b)
        if inv_sum < 1:
            profit_percent = round((1 - inv_sum) * 100, 2)
            return profit_percent
    except:
        return 0
    return 0

def normalize_name(name):
    """Normalize match/team name for comparison"""
    return name.strip().lower().replace(" ", "")

def run_arbitrage():
    global alerts_sent_today, current_day

    # Reset daily alert count
    if datetime.now().day != current_day:
        alerts_sent_today = 0
        current_day = datetime.now().day

    if alerts_sent_today >= MAX_ALERTS_PER_DAY:
        print("Daily alert limit reached.")
        return

    # Fetch data from all 4 bookmakers
    bookmakers_data = (
        get_onexbet_live_odds() + get_onexbet_prematch_odds() +
        get_bcgame_live_odds() + get_bcgame_prematch_odds() +
        get_stake_live_odds() + get_stake_prematch_odds() +
        get_mostbet_live_odds() + get_mostbet_prematch_odds()
    )

    # Compare odds between different bookmakers
    for i, match_a in enumerate(bookmakers_data):
        for match_b in bookmakers_data[i+1:]:
            if match_a["bookmaker"] != match_b["bookmaker"] and normalize_name(match_a["match"]) == normalize_name(match_b["match"]):
                for side in match_a["odds"]:
                    if side in match_b["odds"]:
                        profit = calculate_profit(match_a["odds"][side], match_b["odds"][side])
                        if profit >= 10:
                            match_type = "🟢 Live" if match_a["type"].lower() == "live" else "🔵 Prematch"
                            time_now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                            message = (
                                f"{match_type} Arbitrage Found!\n"
                                f"⚫ {match_a['bookmaker']}: {match_a['odds'][side]}  vs  "
                                f"⚫ {match_b['bookmaker']}: {match_b['odds'][side]}\n"
                                f"💰 Profit: {profit}%\n"
                                f"⏰ {time_now}"
                            )
                            send_telegram_alert(message)
                            alerts_sent_today += 1
                            if alerts_sent_today >= MAX_ALERTS_PER_DAY:
                                return

if __name__ == "__main__":
    print("Bot started - running arbitrage checks...")
    run_arbitrage()
