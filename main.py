# Trigger auto-deploy on Render
# main.py

import os
import time
from datetime import datetime
from telegram import Bot

# Telegram setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# Dummy arbitrage data (replace with real scraping logic)
def get_arbitrage_data():
    return {
        "type": "LIVE",
        "bookmakers": [
            {"name": "1xBet", "odds": 2.1},
            {"name": "Stake", "odds": 2.2}
        ],
        "profit": 10.5,
        "match": "ABC vs XYZ"
    }

def send_alert(data):
    emojis = {
        "LIVE": "🟢",
        "PREMATCH": "🔵",
        "SAME": "🔴",
        "BOOK": "⚫",
        "PROFIT": "💰",
        "TIME": "⏰"
    }

    time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    message = f"{emojis[data['type']]} {data['type']} Arbitrage Found!\n"
    for bm in data['bookmakers']:
        message += f"{emojis['BOOK']} {bm['name']}: {bm['odds']}\n"
    message += f"{emojis['PROFIT']} Profit: {data['profit']}%\n"
    message += f"{emojis['TIME']} Match: {data['match']}\n"
    message += f"{time_str}"

    bot.send_message(chat_id=CHAT_ID, text=message)

# Auto run every 5 minutes
if __name__ == "__main__":
    while True:
        data = get_arbitrage_data()
        if data['profit'] >= 10:
            send_alert(data)
        time.sleep(300)  # 5 minutes
