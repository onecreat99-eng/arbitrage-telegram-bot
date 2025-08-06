# Trigger auto-deploy on Render
import os
import datetime
import requests
from dotenv import load_dotenv
from oddspedia_scraper import get_oddspedia_surebets
from oddsam_scraper import get_oddsam_odds

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MAX_ALERTS_PER_DAY = 8

sent = set()

def send_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def main():
    alerts = 0
    odds_am = get_oddsam_odds()
    oddsp = get_oddspedia_surebets()

    for arb in odds_am:
        key = (arb['match'], arb['market'], arb['bookmaker1'], arb['bookmaker2'])
        if arb['profit'] >= 10 and key not in sent:
            sent.add(key)
            alerts += 1
            msg = (f"💥 Arbitrage {arb['market']} {arb['match']}\n"
                   f"{arb['bookmaker1']}: {arb['odds1']} | {arb['bookmaker2']}: {arb['odds2']}\n"
                   f"📈 Profit: {arb['profit']}%\n"
                   f"{'🟢 Live' if arb['is_live'] else '🔵 Prematch'}\n"
                   f"🕒 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            send_alert(msg)
        if alerts >= MAX_ALERTS_PER_DAY:
            break

if __name__ == "__main__":
    main()
