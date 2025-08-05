# Trigger auto-deploy on Render
import os, time, requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ALERT_LIMIT_PER_DAY = 4

sent_alerts = set()
alerts_sent_today = 0
today_date = datetime.utcnow().date()

def fetch_odds(): 
    return [
        ("ABC vs XYZ", "1xBet", 2.1, "Stake", 2.2, "live")
    ]

def send_alert(match, b1, o1, b2, o2, profit, match_type):
    now_str = datetime.now().strftime('%I:%M %p')
    header = "🟢 LIVE Arbitrage Found!" if match_type=="live" else "🔵 PREMATCH Arbitrage Found!"
    msg = (
        f"{header}\n"
        f"⚫ {b1}: {o1}\n"
        f"⚫ {b2}: {o2}\n"
        f"💰 Profit: {profit:.1f}%\n"
        f"⏰ Match: {match}\n"
        f"🕒 {now_str}"
    )
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": msg})

while True:
    now = datetime.utcnow()
    if now.date() != today_date:
        today_date = now.date()
        alerts_sent_today = 0

    if alerts_sent_today < ALERT_LIMIT_PER_DAY:
        opportunities = fetch_odds()
        for match, b1, o1, b2, o2, mtype in opportunities:
            profit = (o2/o1 - 1) * 100
            key = f"{match}-{b1}-{o1}-{b2}-{o2}"
            if key not in sent_alerts and profit >= 10:
                send_alert(match, b1, o1, b2, o2, profit, mtype)
                sent_alerts.add(key)
                alerts_sent_today += 1
                break

    time.sleep(60)
