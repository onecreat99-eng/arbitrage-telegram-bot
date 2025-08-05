# Trigger auto-deploy on Render
import os
import time
import random
from datetime import datetime
from dotenv import load_dotenv
import requests
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Count for daily limit
alert_count = 0

# Max alerts per day
MAX_ALERTS_PER_DAY = 8

# Minimum profit %
MIN_PROFIT = 10.0

def get_arbitrage_opportunities():
    # ⛏️ Dummy arbitrage logic (replace with real scraping)
    opportunities = []

    # Simulated data
    bookmakers = ["⚫ 1xBet", "⚫ Mostbet", "⚫ Stake", "⚫ BC.Game", "⚫ VBet"]
    market = "Match Winner"
    teams = ["Team A vs Team B", "Team C vs Team D", "Team E vs Team F"]

    if random.random() < 0.5:  # Random chance to find opportunity
        match = random.choice(teams)
        book1 = random.choice(bookmakers)
        book2 = random.choice(bookmakers)
        odds1 = round(random.uniform(2.0, 3.5), 2)
        odds2 = round(random.uniform(2.0, 3.5), 2)
        profit = (1 / odds1 + 1 / odds2)

        if profit < 1:
            profit_percent = round((1 - profit) * 100, 2)
            opportunities.append({
                "match": match,
                "market": market,
                "book1": book1,
                "odds1": odds1,
                "book2": book2,
                "odds2": odds2,
                "profit_percent": profit_percent,
                "same_bookmaker": book1 == book2,
                "match_type": random.choice(["🟢 Live", "🔵 Prematch"])
            })

    return opportunities

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_and_send_alerts():
    global alert_count

    if alert_count >= MAX_ALERTS_PER_DAY:
        print("✅ Daily limit reached. No more alerts today.")
        return

    opportunities = get_arbitrage_opportunities()

    for opp in opportunities:
        if opp["profit_percent"] >= MIN_PROFIT and alert_count < MAX_ALERTS_PER_DAY:
            now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
            message = (
                f"{opp['match_type']} *{opp['match']}*\n\n"
                f"*Market:* {opp['market']}\n"
                f"{opp['book1']} - `{opp['odds1']}`\n"
                f"{opp['book2']} - `{opp['odds2']}`\n"
                f"*Profit:* {opp['profit_percent']}%\n"
                f"*Same Bookmaker:* {'🔴 Yes' if opp['same_bookmaker'] else '🟢 No'}\n"
                f"*Time:* {now}"
            )
            send_telegram_message(message)
            alert_count += 1
            print(f"✅ Sent Alert {alert_count}")

def reset_daily_count():
    global alert_count
    alert_count = 0
    print("🔁 Daily alert counter reset.")

def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_alerts, 'interval', minutes=10)
    scheduler.add_job(reset_daily_count, 'cron', hour=0, minute=0)  # Midnight reset
    scheduler.start()

    print("🚀 Arbitrage bot is running with APScheduler...")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("⛔ Bot stopped.")

if __name__ == "__main__":
    main()
# Keep the app alive (fake web server for Render)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
