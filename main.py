# Trigger auto-deploy on Render
import os import requests from dotenv import load_dotenv from onexbet_live_scraper import get_1xbet_live_odds from onexbet_prematch_scraper import get_1xbet_prematch_odds

Aap yahan baaki scrapers bhi import karenge (Stake, VBet, Mostbet, BC.Game)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

✅ Telegram message formatting

def send_alert(message): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" payload = { "chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown" } requests.post(url, data=payload)

✅ Format message

from datetime import datetime def format_alert(arb): match = arb['match'] market = arb['market'] odds = arb['odds'] profit = arb['profit_percent'] is_live = arb['is_live'] bookmakers = ', '.join([f"⚫{b}" for b in arb['odds'].keys()]) time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")

emoji = '🟢' if is_live else '🔵'
return f"{emoji} *Arbitrage Alert!*

Match: {match} Market: {market} Odds: {odds} Profit: {profit}% Bookmakers: {bookmakers} Time: {time_str}"

✅ Combine all bookmaker odds here

def get_all_odds(): all_odds = [] all_odds.extend(get_1xbet_live_odds()) all_odds.extend(get_1xbet_prematch_odds()) # TODO: add stake, vbet, bc.game, mostbet scrapers return all_odds

✅ Arbitrage detection (basic example: same match, different odds)

def find_arbitrage(all_odds): arbitrages = [] for i in range(len(all_odds)): for j in range(i+1, len(all_odds)): a, b = all_odds[i], all_odds[j] if a['match'] == b['match'] and a['market'] == b['market']: best_odds = { **a['odds'], **b['odds'] } inv_sum = sum([1/o for o in best_odds.values()]) profit_percent = round((1 - inv_sum) * 100, 2) if profit_percent >= 10: arbitrages.append({ "match": a['match'], "market": a['market'], "odds": best_odds, "profit_percent": profit_percent, "is_live": a['is_live'] or b['is_live'] }) return arbitrages

✅ Main function

def main(): all_odds = get_all_odds() arbitrages = find_arbitrage(all_odds) count = 0 for arb in arbitrages: if count >= 8: break send_alert(format_alert(arb)) count += 1

if name == 'main': main()

