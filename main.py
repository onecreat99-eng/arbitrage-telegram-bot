# Trigger auto-deploy on Render
import os
import time
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Sample function to simulate sending a message
def send_telegram_message(text):
    print(f"Sending to Telegram: {text}")

# Simulate arbitrage opportunity detection
def detect_arbitrage():
    return {
        "match": "Team A vs Team B",
        "market": "Match Winner",
        "bookmaker_1": "⚫ 1xBet",
        "bookmaker_2": "⚫ Stake",
        "odds_1": 2.1,
        "odds_2": 2.1,
        "profit_percent": 10.2,
        "match_type": "🔵 Prematch",
        "same_bookmaker": False,
    }

# Main loop
def main():
    opportunity = detect_arbitrage()

    if opportunity and opportunity["profit_percent"] >= 10:
        message = (
            f"{opportunity['match_type']} *{opportunity['match']}*\n"
            f"Market: {opportunity['market']}\n"
            f"{opportunity['bookmaker_1']} - {opportunity['odds_1']}\n"
            f"{opportunity['bookmaker_2']} - {opportunity['odds_2']}\n"
            f"Profit: {opportunity['profit_percent']}%\n"
            f"Same Bookmaker: {'🔴 Yes' if opportunity['same_bookmaker'] else '🟢 No'}\n"
        )
        send_telegram_message(message)

if __name__ == "__main__":
    main()
