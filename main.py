# Trigger auto-deploy on Render
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ===== Dummy Scraper Functions =====
def get_1xbet_odds():
    return [
        {
            "match": "Team A vs Team B",
            "market": "Match Winner",
            "bookmaker": "1xBet",
            "odds": {"Team A": 2.1, "Team B": 1.95},
            "is_live": True
        }
    ]

def get_bcgame_odds():
    return [
        {
            "match": "Team A vs Team B",
            "market": "Match Winner",
            "bookmaker": "BC.Game",
            "odds": {"Team A": 2.2, "Team B": 1.85},
            "is_live": True
        }
    ]

# ===== Telegram Send Function =====
def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

# ===== Arbitrage Detection =====
def check_arbitrage(all_odds):
    alerts = []
    for i in range(len(all_odds)):
        for j in range(i + 1, len(all_odds)):
            a = all_odds[i]
            b = all_odds[j]
            if a["match"] == b["match"] and a["market"] == b["market"] and a["bookmaker"] != b["bookmaker"]:
                try:
                    inv1 = 1 / list(a["odds"].values())[0]
                    inv2 = 1 / list(b["odds"].values())[1]
                    total = inv1 + inv2
                    if total < 1:
                        profit = round((1 - total) * 100, 2)
                        alerts.append({
                            "match": a["match"],
                            "market": a["market"],
                            "profit": profit,
                            "bookmakers": f"{a['bookmaker']} | {b['bookmaker']}",
                            "is_live": a["is_live"] or b["is_live"]
                        })
                except:
                    pass
    return alerts

# ===== MAIN =====
def main():
    all_odds = []
    all_odds.extend(get_1xbet_odds())
    all_odds.extend(get_bcgame_odds())

    arbitrages = check_arbitrage(all_odds)

    for arb in arbitrages:
        if arb["profit"] >= 10:
            emoji = "🟢" if arb["is_live"] else "🔵"
            msg = f"""{emoji} <b>Arbitrage Found!</b>
🏟 Match: {arb['match']}
🎯 Market: {arb['market']}
💰 Profit: {arb['profit']}%
📚 Bookmakers: {arb['bookmakers']}
🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_alert(msg)

if __name__ == "__main__":
    main()
