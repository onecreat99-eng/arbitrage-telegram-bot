# Trigger auto-deploy on Render
import os
import time
from telegram import Bot
from dotenv import load_dotenv
from datetime import datetime
from onexbet_live_scraper import get_1xbet_live_odds

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_alert(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def check_arbitrage():
    matches = get_1xbet_live_odds()
    for match in matches:
        odds1 = match["odds1"]
        odds2 = match["odds2"]
        if odds1 > 2.0 and odds2 > 2.0:
            profit = (1/odds1 + 1/odds2)
            if profit < 1:
                profit_percent = round((1 - profit) * 100, 2)
                now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
                message = (
                    f"🟢 *LIVE Arbitrage Found!*\n\n"
                    f"⚫ 1xBet: {odds1}\n"
                    f"⚫ 1xBet: {odds2}\n"
                    f"💰 Profit: {profit_percent}%\n"
                    f"⏰ Match: {match['team1']} vs {match['team2']}\n"
                    f"🗓️ {now}"
                )
                send_alert(message)

# Run every 2 mins
while True:
    check_arbitrage()
    time.sleep(120)
