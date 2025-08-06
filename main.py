# Trigger auto-deploy on Render
import time
import datetime
import os
from telegram import Bot
from onexbet_scraper import get_onexbet_live_odds, get_onexbet_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from vbet_scraper import get_vbet_live_odds, get_vbet_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

# Telegram Setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Alert Control
MAX_ALERTS_PER_DAY = 8
alert_count = 0
last_reset_date = datetime.date.today()

# Format Bookmaker Name
def format_bookmaker(name):
    return f"⚫ {name}"

# Send Telegram Alert
def send_alert(opportunity):
    global alert_count
    if alert_count >= MAX_ALERTS_PER_DAY:
        return

    match = opportunity['match']
    market = opportunity['market']
    bookmaker = format_bookmaker(opportunity['bookmaker'])
    odds = opportunity['odds']
    profit = opportunity['profit_percent']
    is_live = opportunity['is_live']
    same_bookmaker = opportunity.get('same_bookmaker', False)

    status_emoji = "🟢" if is_live else "🔵"
    same_bookie_emoji = "🔴" if same_bookmaker else "⚪"
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    message = (
        f"{status_emoji} *Arbitrage Opportunity!*\n\n"
        f"*Match:* `{match}`\n"
        f"*Market:* `{market}`\n"
        f"*Odds:* `{odds}`\n"
        f"*Profit:* `{profit:.2f}%`\n"
        f"*Type:* {'Live' if is_live else 'Prematch'}\n"
        f"*Bookmaker:* {bookmaker}\n"
        f"{same_bookie_emoji} *Same Bookmaker:* `{same_bookmaker}`\n"
        f"🕒 `{now}`"
    )

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    alert_count += 1

# Reset alerts daily
def reset_alert_count_if_needed():
    global alert_count, last_reset_date
    today = datetime.date.today()
    if today != last_reset_date:
        alert_count = 0
        last_reset_date = today

# Check for arbitrage opportunities
def find_arbitrage_opportunities(all_odds):
    opportunities = []
    for data in all_odds:
        odds = list(data["odds"].values())
        if len(odds) < 2:
            continue
        inv_sum = sum(1 / o for o in odds if o > 0)
        profit_percent = (1 - inv_sum) * 100
        if profit_percent > 10:
            data["profit_percent"] = profit_percent
            data["same_bookmaker"] = len(set(data["odds"].keys())) == 1
            opportunities.append(data)
    return opportunities

# Combine all scraper odds
def get_all_odds():
    return (
        get_onexbet_live_odds() +
        get_onexbet_prematch_odds() +
        get_stake_live_odds() +
        get_stake_prematch_odds() +
        get_bcgame_live_odds() +
        get_bcgame_prematch_odds() +
        get_vbet_live_odds() +
        get_vbet_prematch_odds() +
        get_mostbet_live_odds() +
        get_mostbet_prematch_odds()
    )

# Main Execution
def main():
    reset_alert_count_if_needed()
    all_odds = get_all_odds()
    opportunities = find_arbitrage_opportunities(all_odds)
    for opp in opportunities:
        if alert_count < MAX_ALERTS_PER_DAY:
            send_alert(opp)
        else:
            break

if __name__ == "__main__":
    main()
