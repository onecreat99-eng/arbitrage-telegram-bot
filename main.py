# Trigger auto-deploy on Render
from flask import Flask
from telegram import Bot
import threading
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

# 🟢 Fake web server for Render
@app.route('/')
def home():
    return 'Bot is running!'

# 🟢 Telegram alert loop
def alert_loop():
    while True:
        try:
            message = "🟢 LIVE Arbitrage Found!\n⚫ 1xBet: 2.1\n⚫ Stake: 2.2\n💰 Profit: 10.5%\n⏰ Match: ABC vs XYZ"
            bot.send_message(chat_id=CHAT_ID, text=message)
            print("Message sent!")
        except Exception as e:
            print("Error:", e)
        time.sleep(3600)  # Alert every 1 hour (adjust as needed)

# 🧵 Start bot loop in background
threading.Thread(target=alert_loop).start()

# 🟢 Run fake web server to satisfy Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
