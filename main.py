# Trigger auto-deploy on Render
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

# Scrapers
from onexbet_scraper import get_onexbet_live_odds, get_onexbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MAX_ALERTS_PER_DAY = 8
PROFIT_THRESHOLD = 10.0

sent_alerts = []

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

def is_duplicate(alert):
    for a in sent_alerts:
        if a['match'] == alert['match'] and a['market'] == alert['market']:
            return True
    return False

def check_arbitrage(odds_data):
    opportunities = []
    for i in range(len(odds_data)):
        for j in range(i+1, len(odds_data)):
            a = odds_data[i]
            b = odds_data[j]
            if a['match'] == b['match'] and a['market'] == b['market'] and a['bookmaker'] != b['bookmaker']:
                try:
                    odds_a = list(a['odds'].values())
                    odds_b = list(b['odds'].values())
                    if len(odds_a) >= 1 and len(odds_b) >= 1:
                        inv1 = 1 / float(odds_a[0])
                        inv2 = 1 / float(odds_b[1]) if len(odds_b) > 1 else 1 / float(odds_b[0])
                        total = inv1 + inv2
                        if total < 1:
                            profit = round((1 - total) * 100, 2)
                            if profit >= PROFIT_THRESHOLD:
                                opportunities.append({
                                    "match": a['match'],
                                    "market": a['market'],
                                    "bookmakers": f"⚫ {a['bookmaker']} | ⚫ {b['bookmaker']}",
                                    "odds": f"{odds_a[0]} | {odds_b[1] if len(odds_b) > 1 else odds_b[0]}",
                                    "profit": profit,
                                    "is_live": a['is_live'] or b['is_live']
                                })
                except:
                    continue
    return opportunities

def format_alert(data):
    match_type = "🟢 Live" if data['is_live'] else "🔵 Prematch"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""{match_type} Arbitrage Found!
🏟️ Match: {data['match']}
🎯 Market: {data['market']}
📊 Odds: {data['odds']}
💰 Profit: {data['profit']}%
📚 Bookmakers: {data['bookmakers']}
🕒 Time: {now}"""

def main():
    global sent_alerts
    sent_alerts = []

    all_odds = []
    all_odds += get_onexbet_live_odds()
    all_odds += get_onexbet_prematch_odds()
    all_odds += get_bcgame_live_odds()
    all_odds += get_bcgame_prematch_odds()

    arbitrage_opportunities = check_arbitrage(all_odds)

    alerts_sent = 0
    for opportunity in arbitrage_opportunities:
        if alerts_sent >= MAX_ALERTS_PER_DAY:
            break
        if not is_duplicate(opportunity):
            message = format_alert(opportunity)
            send_telegram_message(message)
            sent_alerts.append(opportunity)
            alerts_sent += 1
            print(f"Alert Sent: {message}")

if __name__ == "__main__":
    main()
