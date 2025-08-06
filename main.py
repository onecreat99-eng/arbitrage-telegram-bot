import os
import requests
from datetime import datetime
from onexbet import get_onexbet_odds
from stake import get_stake_odds
from bcgame import get_bcgame_odds

# Telegram settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Min profit %
MIN_PROFIT = 10.0
MAX_ALERTS_PER_DAY = 8
alerts_sent_today = 0

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[Telegram ERROR] {e}")

def calc_arbitrage(odds1, odds2):
    try:
        inv_sum = (1/odds1[0]) + (1/odds2[2])
        profit = (1 - inv_sum) * 100
        return profit
    except:
        return -100

def main():
    global alerts_sent_today

    # Collect data
    all_odds = []
    all_odds.extend(get_onexbet_odds())
    all_odds.extend(get_stake_odds())
    all_odds.extend(get_bcgame_odds())

    print(f"Total odds collected: {len(all_odds)}")

    # Arbitrage detection
    for i in range(len(all_odds)):
        for j in range(i + 1, len(all_odds)):
            if alerts_sent_today >= MAX_ALERTS_PER_DAY:
                return

            game1 = all_odds[i]
            game2 = all_odds[j]

            if game1["match"] == game2["match"] and game1["type"] == game2["type"]:
                profit = calc_arbitrage(game1["odds"], game2["odds"])
                if profit >= MIN_PROFIT:
                    msg = (
                        f"{'🟢' if game1['type']=='Live' else '🔵'} <b>{game1['match']}</b>\n"
                        f"📊 Market: {game1['market']}\n"
                        f"⚫ {game1['bookmaker']}: {game1['odds']}\n"
                        f"⚫ {game2['bookmaker']}: {game2['odds']}\n"
                        f"💰 Profit: <b>{profit:.2f}%</b>\n"
                        f"🕒 {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}"
                    )
                    send_telegram_message(msg)
                    alerts_sent_today += 1

if __name__ == "__main__":
    main()
