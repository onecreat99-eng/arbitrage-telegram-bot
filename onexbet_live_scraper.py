# onexbet_live_scraper.py

import requests

def get_1xbet_live_odds():
    url = "https://1xbet.com/LineFeed/Get1x2_VZip?sports=1&count=20&lng=en&cfview=0&mode=4"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        results = []
        for event in data.get("Value", []):
            team1 = event.get("O1", "Team A")
            team2 = event.get("O2", "Team B")
            match_name = f"{team1} vs {team2}"
            odds_data = event.get("E", [])

            if len(odds_data) >= 2:
                odds = {
                    team1: float(odds_data[0].get("C", 0)),
                    team2: float(odds_data[1].get("C", 0))
                }

                # Simple arbitrage calculation
                inv_1 = 1 / odds[team1] if odds[team1] != 0 else 1
                inv_2 = 1 / odds[team2] if odds[team2] != 0 else 1
                total_inv = inv_1 + inv_2
                profit_percent = round((1 - total_inv) * 100, 2)

                if profit_percent > 10:
                    results.append({
                        "match": match_name,
                        "market": "Match Winner",
                        "bookmaker": "1xBet",
                        "odds": odds,
                        "profit_percent": profit_percent,
                        "is_live": True
                    })

        return results

    except Exception as e:
        print("Error fetching live odds from 1xBet:", e)
        return []
