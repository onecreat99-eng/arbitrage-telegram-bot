# Trigger auto-deploy on Render
import time from onexbet import get_onexbet_live_odds, get_onexbet_prematch_odds from stake import get_stake_live_odds, get_stake_prematch_odds from bcgame import get_bcgame_live_odds, get_bcgame_prematch_odds from mostbet import get_mostbet_live_odds, get_mostbet_prematch_odds from telegram_alert import send_telegram_alert

def find_arbitrage_opportunities(all_odds): alerts_sent = 0 max_alerts = 4 now = time.strftime('%d-%m-%Y %H:%M:%S')

for i, match1 in enumerate(all_odds):
    for j, match2 in enumerate(all_odds):
        if i >= j:
            continue
        if match1['match'] != match2['match']:
            continue

        for bet1 in match1['odds']:
            for bet2 in match2['odds']:
                if bet1['market'] != bet2['market']:
                    continue
                if bet1['outcome'] == bet2['outcome']:
                    continue

                try:
                    o1 = float(bet1['odds'])
                    o2 = float(bet2['odds'])
                    profit_percent = (1 / o1 + 1 / o2)

                    if profit_percent < 1:
                        profit = round((1 - profit_percent) * 100, 2)
                        if profit >= 10 and alerts_sent < max_alerts:
                            same_bookmaker = match1['bookmaker'] == match2['bookmaker']
                            match_type = match1['match_type']
                            alert_message = (
                                f"{'🟢' if match_type == 'Live' else '🔵'} {match1['match']}\n"
                                f"📊 Market: {bet1['market']}\n"
                                f"⚫ {match1['bookmaker']}: {bet1['outcome']} @ {o1}\n"
                                f"⚫ {match2['bookmaker']}: {bet2['outcome']} @ {o2}\n"
                                f"💰 Profit: {profit}%\n"
                                f"{'🔴 Same Bookmaker' if same_bookmaker else ''}\n"
                                f"🕒 {now}"
                            )
                            send_telegram_alert(alert_message)
                            alerts_sent += 1
                except:
                    continue

if name == "main": while True: all_odds = [] all_odds += get_onexbet_live_odds() all_odds += get_onexbet_prematch_odds()

all_odds += get_stake_live_odds()
    all_odds += get_stake_prematch_odds()

    all_odds += get_bcgame_live_odds()
    all_odds += get_bcgame_prematch_odds()

    all_odds += get_mostbet_live_odds()
    all_odds += get_mostbet_prematch_odds()

    find_arbitrage_opportunities(all_odds)
    time.sleep(300)  # Check every 5 minutes

