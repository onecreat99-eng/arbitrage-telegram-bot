# Trigger auto-deploy on Render
from onexbet_live_scraper import get_onexbet_live_odds
from onexbet_prematch_scraper import get_onexbet_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from vbet_live_scraper import get_vbet_live_odds
from vbet_prematch_scraper import get_vbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds
from telegram_alert import send_telegram_message
import datetime

MAX_ALERTS_PER_DAY = 8
PROFIT_THRESHOLD = 10.0
sent_alerts = []

def is_duplicate(alert):
    for a in sent_alerts:
        if a['match'] == alert['match'] and a['market'] == alert['market']:
            return True
    return False

def check_arbitrage(odds_data):
    opportunities = []
    for data in odds_data:
        odds = list(data['odds'].values())
        if len(odds) < 2:
            continue
        inverse_sum = sum(1 / o for o in odds)
        profit_percent = round((1 - inverse_sum) * 100, 2)
        if profit_percent >= PROFIT_THRESHOLD:
            data['profit_percent'] = profit_percent
            opportunities.append(data)
    return opportunities

def format_alert(data):
    match_type = "🟢 Live" if data['is_live'] else "🔵 Prematch"
    same_bookmaker = "🔴 Same Bookmaker" if all(v == list(data['odds'].values())[0] for v in data['odds'].values()) else ""
    odds_text = " ".join([f"⚫{k}: {v}" for k, v in data['odds'].items()])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{match_type} | {same_bookmaker}\n🏟️ Match: {data['match']}\n🎯 Market: {data['market']}\n💰 Odds: {odds_text}\n📈 Profit: {data['profit_percent']}%\n🕒 Time: {now}"

def main():
    global sent_alerts
    sent_alerts = []

    all_odds = []
    all_odds += get_onexbet_live_odds()
    all_odds += get_onexbet_prematch_odds()
    all_odds += get_stake_live_odds()
    all_odds += get_stake_prematch_odds()
    all_odds += get_vbet_live_odds()
    all_odds += get_vbet_prematch_odds()
    all_odds += get_bcgame_live_odds()
    all_odds += get_bcgame_prematch_odds()
    all_odds += get_mostbet_live_odds()
    all_odds += get_mostbet_prematch_odds()

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

if __name__ == "__main__":
    main()
