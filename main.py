import os
import telegram
from dotenv import load_dotenv
import time

# ✅ Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

while True:
    message = "✅ Bot is working! Arbitrage alert will be added here."
    bot.send_message(chat_id=CHAT_ID, text=message)
    time.sleep(3600)  # Sends message every hour (for demo)
