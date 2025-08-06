import os
import time
import threading
import requests
from datetime import datetime
from flask import Flask

# ===== IMPORT SCRAPERS =====
from onexbet import get_1xbet_live_odds, get_1xbet_prematch_odds
from stake import get_stake_live_odds, get_stake_prematch_odds
from bcgame import get_bcgame_live_odds, get_bcgame_prematch_odds

# ===== TELEGRAM CONFIG =====
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===== FLASK APP =====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Arbitrage Bot is running..."

# ===== TELEGRAM ALERT FUNCTION =====
def send_telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("[Telegram] Missing BOT_TOKEN or CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        res = requests.post(url, data=payload)
        if res.status_code != 200:
            print("[Telegram] Error:", res.text)
    except Exception as e:
        print(f"[Telegram] Error: {e}")

# ===== PROFIT CALCULATION =====
def calculate_profit(odds_a, odds_b):
    try:
        inv_a = 1 / float(odds_a)
        inv_b = 1 / float(odds_b)
        return round((1 - (inv_a + inv_b)) * 100, 2)
    except:
        return -100

# ===== MAIN BOT LOGIC =====
def run_bot():
    try:
        print(f"[{datetime.now()}] Checking odds...")

        data = (
            get_1xbet_live_odds() + get_1xbet_prematch_odds() +
            get_stake_live_odds() + get_stake_prematch_odds() +
            get_bcgame_live_odds() + get_bcgame_prematch_odds()
        )

        alerts_sent = 0

        for i, match_a in enumerate(data):
            for match_b in data[i + 1:]:
                if (
                    match_a["match"] == match_b["match"] and
                    match_a["market"] == match_b["market"] and
                    match_a["bookmaker"] != match_b["bookmaker"]
                ):
                    for team in match_a["odds"]:
                        if team in match_b["odds"] and match_a["odds"][team] and match_b["odds"][team]:
                            profit = calculate_profit(match_a["odds"][team], match_b["odds"][team])
                            if profit >= 10:
                                match_type = "🟢 Live" if match_a["is_live"] else "🔵 Prematch"
                                time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                message = (
                                    f"{match_type} Arbitrage Found\n"
                                    f"{match_a['bookmaker']}: {match_a['odds'][team]}\n"
                                    f"{match_b['bookmaker']}: {match_b['odds'][team]}\n"
                                    f"💰 Profit: {profit}%\n"
                                    f"🏟 Match: {match_a['match']}\n"
                                    f"📊 Market: {match_a['market']}\n"
                                    f"🕒 {time_now}"
                                )
                                send_telegram_alert(message)
                                alerts_sent += 1
                                if alerts_sent >= 8:
                                    return
    except Exception as e:
        print(f"[Bot Error] {e}")

# ===== BACKGROUND THREAD =====
def start_scheduler():
    while True:
        run_bot()
        time.sleep(300)  # 5 minutes

# ===== START EVERYTHING =====
if __name__ == "__main__":
    threading.Thread(target=start_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
