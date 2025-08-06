# Trigger auto-deploy on Render
import os
import requests
import pytz
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def send_alert():
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = now.strftime("%H:%M:%S %d-%m-%Y")
    
    message = f"""
🟢 *Live Arbitrage Alert*
⚫ *1xBet* 🆚 ⚫ *Mostbet*

💹 *Market:* Full Time Result
📊 *Profit:* 12.5%
⏰ *Time:* {current_time}
"""
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

scheduler = BlockingScheduler()
scheduler.add_job(send_alert, 'interval', minutes=5)
send_alert()  # Run once at start
scheduler.start()
