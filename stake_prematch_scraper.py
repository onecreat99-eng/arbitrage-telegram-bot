def get_stake_prematch_odds():
    url = "https://api.stake.com/api/events/sportsbook?preMatchOnly=true"
    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        odds_list = []

        for event in data['events']:
            match_name = event.get('name', 'Unknown Match')
            markets = event.get('markets', [])
            for market in markets:
                if market.get('name') == "Match Winner":
                    outcomes = market.get('outcomes', [])
                    odds = {}
                    for outcome in outcomes:
                        label = outcome.get('label')
                        price = outcome.get('odds')
                        if label and price:
                            odds[label] = price / 1000  # Stake odds are *1000

                    if len(odds) >= 2:
                        odds_list.append({
                            "match": match_name,
                            "market": "Match Winner",
                            "bookmaker": "Stake",
                            "odds": odds,
                            "profit_percent": 0.0,  # Will be calculated later
                            "is_live": False
                        })

        return odds_list

    except Exception as e:
        print("Stake prematch fetch error:", e)
        return []
