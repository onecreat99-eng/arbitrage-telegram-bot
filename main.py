# Trigger auto-deploy on Render
import time
from onexbet_scraper import get_onexbet_live_odds, get_onexbet_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds
from telegram_alert import send_telegram_alert

def find_arbitrage_opportunities(bookmaker_data):
    opportunities = []

    for i in range(len(bookmaker_data)):
        for j in range(i + 1, len(bookmaker_data)):
            data1 = bookmaker_data[i]
            data2 = bookmaker_data[j]

            if data1["match"].lower() == data2["match"].lower():
                for odd1 in data1["odds"]:
                    for odd2 in data2["odds"]:
                        if (
                            odd1["market"].lower() == odd2["market"].lower()
                            and odd1["outcome"].lower() != odd2["outcome"].lower()
                        ):
                            try:
                                o1 = float(odd1["odds"])
                                o2 = float(odd2["odds"])

                                profit_percent = (1 / o1 + 1 / o2)
                                if profit_percent < 1:
                                    profit = round((1 - profit_percent) * 100, 2)
                                    opportunities.append({
                                        "match": data1["match"],
                                        "market": odd1["market"],
                                        "outcome_1": odd1["outcome"],
                                        "odds_1": o1,
                                        "bookmaker_1": data1["bookmaker"],
                                        "outcome_2": odd2["outcome"],
                                        "odds_2": o2,
                                        "bookmaker_2": data2["bookmaker"],
                                        "match_type": data1["match_type"],
                                        "profit_percent": profit
                                    })
                            except:
                                continue
    return opportunities

def main():
    alerts_sent = 0
    max_alerts_per_day = 4

    while True:
        try:
            all_data = []

            all_data.extend(get_onexbet_live_odds())
            all_data.extend(get_onexbet_prematch_odds())

            all_data.extend(get_stake_live_odds())
            all_data.extend(get_stake_prematch_odds())

            all_data.extend(get_bcgame_live_odds())
            all_data.extend(get_bcgame_prematch_odds())

            all_data.extend(get_mostbet_live_odds())
            all_data.extend(get_mostbet_prematch_odds())

            opportunities = find_arbitrage_opportunities(all_data)

            for arb in opportunities:
                if alerts_sent >= max_alerts_per_day:
                    break
                if arb["profit_percent"] >= 10:
                    send_telegram_alert(arb)
                    alerts_sent += 1

        except Exception as e:
            print("Error in main loop:", e)

        time.sleep(300)  # wait for 5 minutes

if __name__ == "__main__":
    main()
