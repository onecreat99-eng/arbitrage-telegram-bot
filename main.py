# Trigger auto-deploy on Render
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from 1xbet_scraper import get_1xbet_live_odds, get_1xbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PROFIT_THRESHOLD = 10.0
MAX_ALERTS_PER_DAY = 8
sent_alerts = []

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

def is_duplicate(alert):
    return any(a['match'] == alert['match'] and a['market'] == alert['market'] for a in sent_alerts)

def find_arbitrage(all_odds):
    opportunities = []
    for i in range(len(all_odds)):
        for j in range(i + 1, len(all_odds)):
            a = all_odds[i]
            b = all_odds[j]
            if a['match'] == b['match'] and a['market'] == b['market'] and a['bookmaker'] != b['bookmaker']:
                try:
                    inv1 = 1 / float(list(a['odds'].values())[0])
                    inv2 = 1 / float(list(b['odds'].values())[0])
                    total = inv1 + inv2
                    if total < 1:
                        profit = round((1 - total) * 100, 2)
                        if profit >= PROFIT_THRESHOLD:
                            opportunities.append({
                                "match": a['match'],
                                "market": a['market'],
                                "odds": f"⚫ {a['bookmaker']}: {list(a['odds'].values())[0]} | ⚫ {b['bookmaker']}: {list(b['odds'].values())[0]}",
                                "profit": profit,
                                "is_live": a['is_live'] or b['is_live']
                            })
                except:
                    continue
    return opportunities

def format_alert(opportunity):
    emoji = "🟢 Live" if opportunity['is_live'] else "🔵 Prematch"
    time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    return f"""{emoji} Arbitrage Found!
🏟 Match: {opportunity['match']}
🎯 Market: {opportunity['market']}
💰 Odds: {opportunity['odds']}
📈 Profit: {opportunity['profit']}%
⏰ Time: {time_str}"""

def main():
    global sent_alerts
    all_odds = []
    all_odds += get_1xbet_live_odds()
    all_odds += get_1xbet_prematch_odds()
    all_odds += get_bcgame_live_odds()
    all_odds += get_bcgame_prematch_odds()

    arbitrages = find_arbitrage(all_odds)
    alerts_sent = 0
    for arb in arbitrages:
        if alerts_sent >= MAX_ALERTS_PER_DAY:
            break
        if not is_duplicate(arb):
            send_telegram_message(format_alert(arb))
            sent_alerts.append(arb)
            alerts_sent += 1

if __name__ == "__main__":
    main()
