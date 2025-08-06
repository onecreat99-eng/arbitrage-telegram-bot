# Trigger auto-deploy on Render
import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Telegram send function
def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print("Telegram Error:", e)

# ✅ Dummy functions - यहां आप Oddspedia और Odds.am scraping लगा सकते हो
def get_1xbet_data():
    return [
        {"match": "Team A vs Team B", "market": "Match Winner", "bookmaker": "1xBet", "odds": 2.1, "is_live": True}
    ]

def get_bcgame_data():
    return [
        {"match": "Team A vs Team B", "market": "Match Winner", "bookmaker": "BC.Game", "odds": 2.2, "is_live": True}
    ]

# ✅ Arbitrage detection
def check_arbitrage(data1, data2):
    arbitrages = []
    for a in data1:
        for b in data2:
            if a['match'] == b['match'] and a['market'] == b['market'] and a['bookmaker'] != b['bookmaker']:
                inv1 = 1 / a['odds']
                inv2 = 1 / b['odds']
                total = inv1 + inv2
                if total < 1:
                    profit = round((1 - total) * 100, 2)
                    arbitrages.append({
                        "match": a['match'],
                        "market": a['market'],
                        "odds": f"{a['bookmaker']} {a['odds']} | {b['bookmaker']} {b['odds']}",
                        "profit": profit,
                        "is_live": a['is_live'] or b['is_live']
                    })
    return arbitrages

# ✅ Loop for continuous checking
def main():
    while True:
        one_x = get_1xbet_data()
        bc_game = get_bcgame_data()
        arbs = check_arbitrage(one_x, bc_game)

        for arb in arbs:
            if arb['profit'] >= 10:
                emoji = "🟢" if arb['is_live'] else "🔵"
                now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
                msg = f"""{emoji} Arbitrage Alert!
🏟️ Match: {arb['match']}
🎯 Market: {arb['market']}
💰 Odds: {arb['odds']}
📈 Profit: {arb['profit']}%
🕒 Time: {now}"""
                send_alert(msg)

        print(f"[{datetime.now()}] Checked arbitrage. Sleeping 5 mins...")
        time.sleep(300)  # 5 min wait

if __name__ == "__main__":
    main()
