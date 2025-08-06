# Trigger auto-deploy on Render
# Trigger auto-deploy on Render
import os
from dotenv import load_dotenv

# ✅ Import sabhi scrapers
from onexbet_live_scraper import get_1xbet_live_odds
from onexbet_prematch_scraper import get_1xbet_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from vbet_scraper import get_vbet_live_odds, get_vbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Telegram message formatting
def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        import requests
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

# ✅ Format message
from datetime import datetime
def format_alert(arb):
    match = arb['match']
    market = arb['market']
    odds = arb['odds']
    profit = arb['profit']
    bookmakers = arb['bookmakers']
    is_live = arb['is_live']
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji = '🟢' if is_live else '🔵'
    return f"""{emoji} *Arbitrage Alert!*

Match: {match}
Market: {market}
Odds: {odds}
Profit: {profit}%
Bookmakers: {bookmakers}
Time: {time_str}"""

# ✅ Collect all odds from all bookmakers
def get_all_odds():
    all_odds = []
    all_odds.extend(get_1xbet_live_odds())
    all_odds.extend(get_1xbet_prematch_odds())
    all_odds.extend(get_stake_live_odds())
    all_odds.extend(get_stake_prematch_odds())
    all_odds.extend(get_vbet_live_odds())
    all_odds.extend(get_vbet_prematch_odds())
    all_odds.extend(get_mostbet_live_odds())
    all_odds.extend(get_mostbet_prematch_odds())
    all_odds.extend(get_bcgame_live_odds())
    all_odds.extend(get_bcgame_prematch_odds())
    return all_odds

# ✅ Arbitrage detection
def find_arbitrage(all_odds):
    arbitrages = []
    for i in range(len(all_odds)):
        for j in range(i+1, len(all_odds)):
            a = all_odds[i]
            b = all_odds[j]
            if a['match'] == b['match'] and a['market'] == b['market'] and a['bookmaker'] != b['bookmaker']:
                try:
                    inv1 = 1 / float(a['odds'])
                    inv2 = 1 / float(b['odds'])
                    total = inv1 + inv2
                    if total < 1:
                        profit = round((1 - total) * 100, 2)
                        arbitrages.append({
                            'match': a['match'],
                            'market': a['market'],
                            'odds': f"{a['odds']} | {b['odds']}",
                            'profit': profit,
                            'bookmakers': f"⚫ {a['bookmaker']} | ⚫ {b['bookmaker']}",
                            'is_live': a['is_live'] or b['is_live']
                        })
                except:
                    continue
    return arbitrages

# ✅ Main function
def main():
    all_odds = get_all_odds()
    arbitrages = find_arbitrage(all_odds)
    count = 0
    for arb in arbitrages:
        if arb['profit'] >= 10:
            send_alert(format_alert(arb))
            count += 1
        if count >= 8:
            break

if __name__ == "__main__":
    main()
