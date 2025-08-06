# Trigger auto-deploy on Render
import time
from datetime import datetime
import os
import telegram

from onexbet_scraper import get_onexbet_live_odds, get_onexbet_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from vbet_scraper import get_vbet_live_odds, get_vbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

# ✅ Telegram Bot Setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

# ✅ Alert Limit Config
MAX_ALERTS_PER_DAY = 8
alert_count = 0
last_alert_date = datetime.now().date()

# ✅ Telegram Alert Function
def send_alert(message):
    global alert_count, last_alert_date

    today = datetime.now().date()
    if today != last_alert_date:
        alert_count = 0
        last_alert_date = today

    if alert_count < MAX_ALERTS_PER_DAY:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.HTML)
        alert_count += 1

# ✅ Arbitrage Check Function
def detect_arbitrage(all_odds):
    opportunities = []
    for match_group in all_odds:
        match_dict = {}
        for odd in match_group:
            match_key = (odd['match'], odd['market'], odd['is_live'])
            if match_key not in match_dict:
                match_dict[match_key] = []
            match_dict[match_key].append(odd)

        for key, odds_list in match_dict.items():
            best_odds = {}
            for odd in odds_list:
                for outcome, value in odd['odds'].items():
                    if outcome not in best_odds or value > best_odds[outcome]['value']:
                        best_odds[outcome] = {'value': value, 'bookmaker': odd['bookmaker']}

            if len(best_odds) >= 2:
                inv_total = sum(1 / odd['value'] for odd in best_odds.values())
                if inv_total < 1:
                    profit_percent = round((1 - inv_total) * 100, 2)
                    if profit_percent >= 10:
                        match_name, market, is_live = key
                        message = f"""
{"🟢 Live Match" if is_live else "🔵 Prematch"} Arbitrage Opportunity

🏟️ Match: <b>{match_name}</b>
🎯 Market: <b>{market}</b>
📊 Profit: <b>{profit_percent}%</b>

⚫ Bookmakers:
""" + "\n".join(
    [f"⚫ <b>{outcome}</b>: {data['value']} ({data['bookmaker']})"
     for outcome, data in best_odds.items()]
) + f"""

🕒 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
                        """
                        opportunities.append(message.strip())

    return opportunities

# ✅ Run Bot
def run_bot():
    all_odds = []

    # Add odds from all scrapers here
    all_odds.append([
        *get_onexbet_live_odds(),
        *get_stake_live_odds(),
        *get_vbet_live_odds(),
        *get_bcgame_live_odds(),
        *get_mostbet_live_odds()
    ])

    all_odds.append([
        *get_onexbet_prematch_odds(),
        *get_stake_prematch_odds(),
        *get_vbet_prematch_odds(),
        *get_bcgame_prematch_odds(),
        *get_mostbet_prematch_odds()
    ])

    arbitrage_opps = detect_arbitrage(all_odds)
    for opp in arbitrage_opps:
        send_alert(opp)
        time.sleep(1)

if __name__ == "__main__":
    run_bot()
