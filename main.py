import os
import requests
from datetime import datetime
from onexbet import get_1xbet_live_odds, get_1xbet_prematch_odds
from stake import get_stake_live_odds, get_stake_prematch_odds
from bcgame import get_bcgame_live_odds, get_bcgame_prematch_odds

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MAX_ALERTS_PER_DAY = 8
alerts_sent_today = 0
today_date = datetime.now().date()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_arbitrage():
    global alerts_sent_today, today_date

    if datetime.now().date() != today_date:
        alerts_sent_today = 0
        today_date = datetime.now().date()

    if alerts_sent_today >= MAX_ALERTS_PER_DAY:
        print("Max alerts reached for today.")
        return

    bookmakers_data = {
        "⚫ 1xBet": get_1xbet_live_odds() + get_1xbet_prematch_odds(),
        "⚫ Stake": get_stake_live_odds() + get_stake_prematch_odds(),
        "⚫ BC.Game": get_bcgame_live_odds() + get_bcgame_prematch_odds()
    }

    for match in bookmakers_data["⚫ 1xBet"]:
        match_name = match["match"]
        market = match["market"]
        odds_1xbet = match["odds"]

        for book, matches in bookmakers_data.items():
            for m in matches:
                if m["match"] == match_name and m["market"] == market:
                    highest_odds = max(odds_1xbet, m["odds"])
                    profit_percent = (highest_odds / odds_1xbet - 1) * 100

                    if profit_percent >= 10 and alerts_sent_today < MAX_ALERTS_PER_DAY:
                        message = (
                            f"{'🟢' if 'Live' in market else '🔵'} <b>{match_name}</b>\n"
                            f"📊 Market: {market}\n"
                            f"{book} Odds: {m['odds']}\n"
                            f"⚫ 1xBet Odds: {odds_1xbet}\n"
                            f"💰 Profit: {profit_percent:.2f}%\n"
                            f"⏰ {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}"
                        )
                        send_telegram_message(message)
                        alerts_sent_today += 1

if __name__ == "__main__":
    print("Bot started")
    check_arbitrage()
