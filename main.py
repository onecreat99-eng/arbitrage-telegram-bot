# Trigger auto-deploy on Render
import os
import time
import requests
from datetime import datetime

# Telegram config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_all_arbitrage_data():
    # Dummy arbitrage data (real scraper baad me add hoga)
    return [
        {
            "team1": "Team A",
            "team2": "Team B",
            "market": "Match Winner",
            "bookmaker_1": "Stake",
            "bookmaker_2": "1xBet",
            "odds_1": 2.10,
            "odds_2": 1.95,
            "match_type": "Live",
            "profit": 12.5
        },
        {
            "team1": "Team C",
            "team2": "Team D",
            "market": "Total Goals Over/Under",
            "bookmaker_1": "Mostbet",
            "bookmaker_2": "VBet",
            "odds_1": 2.20,
            "odds_2": 1.90,
            "match_type": "Prematch",
            "profit": 10.3
        }
    ]

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    print("Message sent:", response.status_code)

def format_alert(arb):
    match_name = f"{arb['team1']} vs {arb['team2']}"
    market = arb.get("market", "Unknown Market")
    bookmaker_1 = arb['bookmaker_1']
    bookmaker_2 = arb['bookmaker_2']
    odds_1 = arb['odds_1']
    odds_2 = arb['odds_2']
    match_type = arb['match_type']
    profit = arb['profit']

    time_now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    emoji_type = "🟢" if match_type == "Live" else "🔵"

    msg = f"""
{emoji_type} *{match_name}*
📊 Market: *{market}*
⚫ {bookmaker_1}: `{odds_1}`
⚫ {bookmaker_2}: `{odds_2}`
💰 Profit: *{profit}%*
🕒 Type: {match_type}
📅 Time: `{time_now}`
"""
    return msg.strip()

def main():
    arbitrage_data = get_all_arbitrage_data()

    for arb in arbitrage_data:
        if arb["profit"] >= 10:  # only high profit
            message = format_alert(arb)
            send_telegram_alert(message)
            time.sleep(2)

if __name__ == "__main__":
    main()
