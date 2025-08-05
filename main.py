# Trigger auto-deploy on Render
from onexbet_live_scraper import get_1xbet_live_odds
from datetime import datetime
import asyncio
from telegram import Bot

BOT_TOKEN = "your_token"
CHAT_ID = "your_chat_id"

bot = Bot(token=BOT_TOKEN)

async def send_alert():
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    arbitrage_data = get_1xbet_live_odds()

    for arb in arbitrage_data:
        message = f"""
🟢 *Live Arbitrage Alert!*

⚫ *Match:* {arb['match']}
⚫ *Market:* {arb['market']}
⚫ *Bookmaker:* ⚫{arb['bookmaker']}
⚫ *Odds:* {arb['odds']}
⚫ *Profit:* {arb['profit_percent']}%
⚫ *Time:* {now}
"""
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

asyncio.run(send_alert())
