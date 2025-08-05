# Trigger auto-deploy on Render
import requests
import datetime
import os
import time
import telegram
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

alerts_sent_today = 0
today_date = datetime.datetime.utcnow().date()

MAX_ALERTS_PER_DAY = 4  # Render free plan limit

def get_live_odds_from_1xbet():
    # Dummy data, replace with real scraping logic
    return [
        {"match": "Team A vs Team B", "market": "1x2", "bookmaker": "1xBet", "selection": "Team A", "odds": 2.1},
    ]

def get_live_odds_from_mostbet():
    return [
        {"match": "Team A vs Team B", "market": "1x2", "bookmaker": "Mostbet", "selection": "Team B", "odds": 2.3},
    ]

def get_live_odds_from_bcgame():
    return []

def get_live_odds_from_stake():
    return []

def get_live_odds_from_vbet():
    return []

def find_arbitrage(odds_list):
    opportunities = []
    matches = {}
    for odd in odds_list:
        key = (odd["match"], odd["market"])
        if key not in matches:
            matches[key] = []
        matches[key].append(odd)

    for match_key, odds in matches.items():
        if len(odds) < 2:
            continue
        best_odds = {}
        for odd in odds:
            selection = odd["selection"]
            if selection not in best_odds or odd["odds"] > best_odds[selection]["odds"]:
                best_odds[selection] = odd

        if len(best_odds) < 2:
            continue

        inverse_sum = sum(1 / v["odds"] for v in best_odds.values())
        profit_percent = (1 - inverse_sum) * 100
        if profit_percent > 10:
            opportunities.append((match_key, best_odds, round(profit_percent, 2)))

    return opportunities

def send_telegram_alert(match_key, best_odds, profit):
    match, market = match_key
    global alerts_sent_today

    if alerts_sent_today >= MAX_ALERTS_PER_DAY:
        return

    msg = f"🟢 *Live Arbitrage Alert!*\n"
    msg += f"*Match:* {match}\n"
    msg += f"*Market:* {market}\n"
    msg += f"*Profit:* {profit}%\n"

    for sel, data in best_odds.items():
        msg += f"⚫ *{data['bookmaker']}* ➤ {sel}: {data['odds']}\n"

    msg += f"*Time:* {datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}"

    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
    alerts_sent_today += 1

def main():
    global today_date, alerts_sent_today

    while True:
        now = datetime.datetime.utcnow().date()
        if now != today_date:
            today_date = now
            alerts_sent_today = 0

        try:
            odds = []
            odds += get_live_odds_from_1xbet()
            odds += get_live_odds_from_mostbet()
            odds += get_live_odds_from_bcgame()
            odds += get_live_odds_from_stake()
            odds += get_live_odds_from_vbet()

            arbitrages = find_arbitrage(odds)
            for arb in arbitrages:
                send_telegram_alert(*arb)
        except Exception as e:
            print("Error:", e)

        time.sleep(60)

if __name__ == "__main__":
    main()
