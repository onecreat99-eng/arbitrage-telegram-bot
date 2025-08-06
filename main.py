import os
import time
import requests
from datetime import datetime

# ============ TELEGRAM CONFIG ============
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ============ SETTINGS ============
MAX_ALERTS_PER_DAY = 8
PROFIT_THRESHOLD = 10  # %
alerts_sent_today = 0
today_date = datetime.now().date()

# ============ SCRAPER PLACEHOLDERS ============

def get_1xbet_live_odds():
    return []  # TODO: Add real scraping code

def get_1xbet_prematch_odds():
    return []  # TODO: Add real scraping code

def get_stake_live_odds():
    return []  # TODO: Add real scraping code

def get_stake_prematch_odds():
    return []  # TODO: Add real scraping code

def get_bcgame_live_odds():
    return []  # TODO: Add real scraping code

def get_bcgame_prematch_odds():
    return []  # TODO: Add real scraping code

# ============ TELEGRAM ALERT ============

def send_telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("[Telegram] Missing BOT_TOKEN or CHAT_ID")
        return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
    except Exception as e:
        print(f"[Telegram] Error: {e}")

# ============ ARBITRAGE CHECK ============
def calculate_profit(odds_a, odds_b):
    try:
        inv_a = 1 / float(odds_a)
        inv_b = 1 / float(odds_b)
        return round((1 - (inv_a + inv_b)) * 100, 2)
    except:
        return -100

def run_bot():
    global alerts_sent_today, today_date

    # Reset daily alert count
    if datetime.now().date() != today_date:
        alerts_sent_today = 0
        today_date = datetime.now().date()

    if alerts_sent_today >= MAX_ALERTS_PER_DAY:
        print("Max alerts sent today.")
        return

    # Get all odds (currently empty lists)
    data = (
        get_1xbet_live_odds() + get_1xbet_prematch_odds() +
        get_stake_live_odds() + get_stake_prematch_odds() +
        get_bcgame_live_odds() + get_bcgame_prematch_odds()
    )

    # Compare for arbitrage
    for i, match_a in enumerate(data):
        for match_b in data[i + 1:]:
            if match_a["match"] == match_b["match"] and match_a["market"] == match_b["market"]:
                for team in match_a["odds"]:
                    if team in match_b["odds"]:
                        profit = calculate_profit(match_a["odds"][team], match_b["odds"][team])
                        if profit >= PROFIT_THRESHOLD:
                            match_type = "🟢 Live" if match_a["is_live"] else "🔵 Prematch"
                            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            message = (
                                f"{match_type} Arbitrage Found!\n"
                                f"{match_a['bookmaker']}: {match_a['odds'][team]}\n"
                                f"{match_b['bookmaker']}: {match_b['odds'][team]}\n"
                                f"💰 Profit: {profit}%\n"
                                f"🕒 {time_now}"
                            )
                            send_telegram_alert(message)
                            alerts_sent_today += 1
                            if alerts_sent_today >= MAX_ALERTS_PER_DAY:
                                return

# ============ MAIN LOOP ============
if __name__ == "__main__":
    print("Bot started. Running every 5 minutes...")
    while True:
        run_bot()
        time.sleep(300)
