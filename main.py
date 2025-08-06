# Trigger auto-deploy on Render
# main.py
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Config
MAX_ALERTS_PER_DAY = 8
PROFIT_THRESHOLD = 10.0

sent_alerts = []

# ----------------- SCRAPERS -----------------

def get_oddspedia_odds():
    """Scrape from Oddspedia API"""
    url = "https://api.oddspedia.com/v1/matches?bookmakers=stake,bcgame"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        matches = []
        for match in data.get("matches", []):
            matches.append({
                "match": match.get("name", "Unknown Match"),
                "market": "Match Winner",
                "bookmaker": "Oddspedia",
                "odds": {
                    "Team1": match.get("odds", {}).get("team1", 0),
                    "Team2": match.get("odds", {}).get("team2", 0)
                },
                "is_live": match.get("status", "") == "live"
            })
        return matches
    except Exception as e:
        print("Oddspedia Error:", e)
        return []

def get_oddsam_odds():
    """Scrape from Odds.am API"""
    url = "https://odds.am/api/v2/events?bookmakers=stake,bcgame"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        matches = []
        for match in data.get("events", []):
            matches.append({
                "match": match.get("name", "Unknown Match"),
                "market": "Match Winner",
                "bookmaker": "Odds.am",
                "odds": {
                    "Team1": match.get("odds", {}).get("team1", 0),
                    "Team2": match.get("odds", {}).get("team2", 0)
                },
                "is_live": match.get("status", "") == "live"
            })
        return matches
    except Exception as e:
        print("Odds.am Error:", e)
        return []

# ----------------- LOGIC -----------------

def send_telegram(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

def is_duplicate(alert):
    for a in sent_alerts:
        if a['match'] == alert['match'] and a['market'] == alert['market']:
            return True
    return False

def check_arbitrage(all_odds):
    arbitrages = []
    for i in range(len(all_odds)):
        for j in range(i+1, len(all_odds)):
            a = all_odds[i]
            b = all_odds[j]
            if a['match'] == b['match'] and a['market'] == b['market'] and a['bookmaker'] != b['bookmaker']:
                try:
                    inv1 = 1 / float(list(a['odds'].values())[0])
                    inv2 = 1 / float(list(b['odds'].values())[1])
                    total = inv1 + inv2
                    if total < 1:
                        profit = round((1 - total) * 100, 2)
                        if profit >= PROFIT_THRESHOLD:
                            arbitrages.append({
                                'match': a['match'],
                                'market': a['market'],
                                'odds': f"{list(a['odds'].values())[0]} | {list(b['odds'].values())[1]}",
                                'profit': profit,
                                'bookmakers': f"⚫ {a['bookmaker']} | ⚫ {b['bookmaker']}",
                                'is_live': a['is_live'] or b['is_live']
                            })
                except:
                    continue
    return arbitrages

def format_alert(arb):
    emoji = '🟢' if arb['is_live'] else '🔵'
    time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    return f"""{emoji} *Arbitrage Found!*
🏟️ Match: {arb['match']}
🎯 Market: {arb['market']}
💰 Odds: {arb['odds']}
📈 Profit: {arb['profit']}%
📚 Bookmakers: {arb['bookmakers']}
⏰ Time: {time_str}"""

# ----------------- MAIN -----------------

def main():
    global sent_alerts
    sent_alerts = []
    all_odds = []
    all_odds += get_oddspedia_odds()
    all_odds += get_oddsam_odds()

    arbitrages = check_arbitrage(all_odds)
    count = 0
    for arb in arbitrages:
        if count >= MAX_ALERTS_PER_DAY:
            break
        if not is_duplicate(arb):
            send_telegram(format_alert(arb))
            sent_alerts.append(arb)
            count += 1

if __name__ == "__main__":
    main()
