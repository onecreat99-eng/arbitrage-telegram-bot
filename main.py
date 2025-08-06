# Trigger auto-deploy on Render
import telebot
import requests
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

sent_alerts = 0  # global count

def get_arbitrage_data():
    # Dummy arbitrage data (replace this with actual scraping logic)
    return [
        {
            "match": "Team A 🆚 Team B",
            "market": "Fulltime Result",
            "odds": {
                "⚫ 1xBet": 2.1,
                "⚫ Mostbet": 1.95
            },
            "profit": 10.4,
            "match_type": "🟢 Live",
            "same_bookmaker": False
        },
        {
            "match": "Team C 🆚 Team D",
            "market": "Over/Under 2.5",
            "odds": {
                "⚫ Stake": 2.05,
                "⚫ VBet": 1.98
            },
            "profit": 11.3,
            "match_type": "🔵 Prematch",
            "same_bookmaker": False
        }
    ]

def send_telegram_alert(data):
    match = data["match"]
    market = data["market"]
    odds = data["odds"]
    profit = data["profit"]
    match_type = data["match_type"]
    same = "🔴 Same Bookmaker" if data["same_bookmaker"] else "🟡 Cross Bookmaker"

    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    time_str = now.strftime("%H:%M:%S | %d-%m-%Y")

    message = (
        f"{match_type} *Arbitrage Alert!*\n\n"
        f"*Match:* {match}\n"
        f"*Market:* {market}\n"
        f"*Odds:* {' vs '.join([f'{k} @ {v}' for k, v in odds.items()])}\n"
        f"*Profit:* {profit:.2f}%\n"
        f"*Type:* {same}\n"
        f"*Time:* {time_str}"
    )
    bot.send_message(CHAT_ID, message, parse_mode="Markdown")

def check_and_send_alerts():
    global sent_alerts
    if sent_alerts >= 4:
        print("🔴 Daily alert limit reached")
        return

    data = get_arbitrage_data()
    for arb in data:
        if arb["profit"] >= 10 and sent_alerts < 4:
            send_telegram_alert(arb)
            sent_alerts += 1
            print(f"✅ Alert sent ({sent_alerts})")
        else:
            print("ℹ️ Skipped: Profit below 10% or limit reached")

def reset_alert_count():
    global sent_alerts
    sent_alerts = 0
    print("🔄 Daily alert count reset")

scheduler = BlockingScheduler(timezone="Asia/Kolkata")
scheduler.add_job(check_and_send_alerts, 'interval', minutes=5)
scheduler.add_job(reset_alert_count, 'cron', hour=0, minute=0)

print("🚀 Bot started...")
scheduler.start()
