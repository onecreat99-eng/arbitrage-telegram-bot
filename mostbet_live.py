# mostbet_live.py

import requests

def get_mostbet_live_odds():
    url = "https://mostbet.com/api/v1/events/list?lang=en&type=live"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        arbitrage_data = []

        for event in data.get('events', []):
            match_name = event.get('name')
            markets = event.get('markets', [])

            for market in markets:
                outcomes = market.get('outcomes', [])
                if len(outcomes) >= 2:
                    team1 = outcomes[0]
                    team2 = outcomes[1]

                    odds1 = float(team1.get('odd', 0))
                    odds2 = float(team2.get('odd', 0))

                    if odds1 > 1 and odds2 > 1:
                        inv_1 = 1 / odds1
                        inv_2 = 1 / odds2
                        total_inv = inv_1 + inv_2
                        profit_percent = round((1 - total_inv) * 100, 2)

                        if profit_percent > 10:
                            arbitrage_data.append({
                                "type": "LIVE",
                                "match": match_name,
                                "market": market.get('name', 'Unknown'),
                                "profit": profit_percent,
                                "bookmakers": [
                                    {"name": "Mostbet", "odds": odds1},
                                    {"name": "Mostbet", "odds": odds2}
                                ]
                            })

        return arbitrage_data

    except Exception as e:
        print(f"[Mostbet Live Error] {e}")
        return []
