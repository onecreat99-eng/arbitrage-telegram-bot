# Trigger auto-deploy on Render
# main.py

import os
import asyncio
from datetime import datetime
from telegram import Bot

# Telegram setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# Dummy arbitrage data (replace this with real scraping logic)
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

# ✅ Make async function with await
async def send_alert(data):
    emojis = {
        "LIVE": "🟢", "PREMATCH": "🔵", "SAME": "🔴",
        "BOOK": "⚫", "PROFIT": "💰", "TIME": "⏰"
    }
    time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    
    message = f"{emojis[data['type']]} {data['type']} Arbitrage Found!\n"
    for bm in data['bookmakers']:
        message += f"{emojis['BOOK']} {bm['name']}: {bm['odds']}\n"
    message += f"{emojis['PROFIT']} Profit: {data['profit']}%\n"
    message += f"{emojis['TIME']} Match: {data['match']}\n"
    message += f"{time_str}"

    await bot.send_message(chat_id=CHAT_ID, text=message)

# ✅ Main function to run everything
async def main():
    data = get_arbitrage_data()
    if data['profit'] >= 10:
        await send_alert(data)

# ✅ Run the async event loop
if __name__ == "__main__":
    asyncio.run(main())
