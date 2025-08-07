import os
import requests
from datetime import datetime
from onexbet import get_1xbet_live_odds, get_1xbet_prematch_odds
from stake import get_stake_live_odds, get_stake_prematch_odds
from bcgame import get_bcgame_live_odds, get_bcgame_prematch_odds

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    """Telegram पर message भेजो"""
    if not BOT_TOKEN or not CHAT_ID:
        print("[Telegram] Missing BOT_TOKEN or CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"[Telegram] Error: {e}")

def calculate_profit(odd_a, odd_b):
    """दो odds से arbitrage profit निकालो"""
    try:
        inv_a = 1 / float(odd_a)
        inv_b = 1 / float(odd_b)
        return round((1 - (inv_a + inv_b)) * 100, 2)
    except:
        return -100

def run_bot():
    """Scrapers चलाओ और arbitrage find करो"""
    try:
        data = (
            get_1xbet_live_odds() + get_1xbet_prematch_odds() +
            get_stake_live_odds() + get_stake_prematch_odds() +
            get_bcgame_live_odds() + get_bcgame_prematch_odds()
        )

        alerts_sent = 0

        for i, match_a in enumerate(data):
            for match_b in data[i + 1:]:
                if match_a["match"] == match_b["match"]:
                    if not match_a["odds"] or not match_b["odds"]:
                        continue
                    try:
                        profit = calculate_profit(match_a["odds"][0], match_b["odds"][1])
                        if profit >= 10:
                            match_type = "🟢 Live" if match_a["type"] == "Live" else "🔵 Prematch"
                            time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            message = (
                                f"{match_type} Arbitrage Found!\n"
                                f"{match_a['match']}\n"
                                f"{match_a.get('type')} Odds: {match_a['odds']}\n"
                                f"{match_b.get('type')} Odds: {match_b['odds']}\n"
                                f"💰 Profit: {profit}%\n"
                                f"🕒 {time_now}"
                            )
                            send_telegram_alert(message)
                            alerts_sent += 1
                            if alerts_sent >= 8:
                                return
                    except:
                        continue
    except Exception as e:
        print(f"[Bot Error] {e}")

if __name__ == "__main__":
    print("Bot started. Checking for arbitrage...")
    run_bot()
