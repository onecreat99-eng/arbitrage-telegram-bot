import os 
import time 
import requests 
from telegram import Bot 
from datetime import datetime

# Load .env manually if needed (for local testing)

from dotenv import load_dotenv load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

Counter for daily limit

alerts_sent_today = 0 max_alerts_per_day = 8 last_reset_day = datetime.now().day

Placeholder: Replace with real scraped data from each bookmaker

def get_odds_from_1xbet(): return [ {"match": "Empoli vs Sassuolo", "market": "Over/Under 2.5", "type": "live", "bookmaker": "1xBet", "odds": {"over": 2.1}}, ]

def get_odds_from_stake(): return [ {"match": "Empoli vs Sassuolo", "market": "Over/Under 2.5", "type": "live", "bookmaker": "Stake", "odds": {"under": 2.0}}, ]

Add similar dummy functions for other bookmakers

def get_odds_from_mostbet(): return [] def get_odds_from_bcgame(): return [] def get_odds_from_vbet(): return []

bookmaker_sources = [ get_odds_from_1xbet, get_odds_from_stake, get_odds_from_mostbet, get_odds_from_bcgame, get_odds_from_vbet, ]

def reset_daily_counter(): global alerts_sent_today, last_reset_day current_day = datetime.now().day if current_day != last_reset_day: alerts_sent_today = 0 last_reset_day = current_day

def send_telegram_alert(data): global alerts_sent_today if alerts_sent_today >= max_alerts_per_day: return

is_live = data['type'] == 'live'
match_emoji = '🟢' if is_live else '🔵'

msg = (
    f"{match_emoji} {data['match']}\n"
    f"📊 Market: {data['market']}\n"
    f"⚫ {data['bookmaker1']} 🆚 ⚫ {data['bookmaker2']}\n"
    f"💰 Odds: {data['odd1']} / {data['odd2']}\n"
    f"📈 Profit: {data['profit']:.2f}%\n"
    f"⏱️ Match Type: {'Live' if is_live else 'Prematch'}\n"
    f"📅 {datetime.now().strftime('%d %B | %I:%M %p')}"
)

bot.send_message(chat_id=CHAT_ID, text=msg)
alerts_sent_today += 1

def detect_arbitrage(): reset_daily_counter() all_data = [] for source in bookmaker_sources: all_data.extend(source())

# Compare every pair
for i in range(len(all_data)):
    for j in range(i + 1, len(all_data)):
        a = all_data[i]
        b = all_data[j]
        if a['match'] != b['match'] or a['market'] != b['market']:
            continue
        if a['bookmaker'] == b['bookmaker']:
            continue

        a_keys = a['odds'].keys()
        b_keys = b['odds'].keys()
        common_keys = list(set(a_keys) & set(b_keys))
        if not common_keys:
            continue

        for key in common_keys:
            odd1 = a['odds'][key]
            odd2 = b['odds'][key]
            inv_sum = (1/odd1) + (1/odd2)
            if inv_sum < 1:
                profit = ((1 / inv_sum) - 1) * 100
                if profit >= 10:
                    send_telegram_alert({
                        "match": a['match'],
                        "market": a['market'],
                        "type": a['type'],
                        "bookmaker1": a['bookmaker'],
                        "bookmaker2": b['bookmaker'],
                        "odd1": odd1,
                        "odd2": odd2,
                        "profit": profit,
                    })

if name == "main": while True: detect_arbitrage() time.sleep(60)

