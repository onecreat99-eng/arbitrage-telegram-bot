import requests

def get_stake_odds(live=True):
    url = "https://api.stake.com/sports/live" if live else "https://api.stake.com/sports/upcoming"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for event in data.get("events", []):
            match_name = event.get("name", "Unknown Match")
            for market in event.get("markets", []):
                odds_dict = {}
                for outcome in market.get("outcomes", []):
                    odds_dict[outcome.get("label", "Unknown")] = float(outcome.get("price", 0))
                if odds_dict:
                    results.append({
                        "match": match_name,
                        "market": market.get("name", "Unknown Market"),
                        "bookmaker": "⚫ Stake",
                        "odds": odds_dict,
                        "is_live": live
                    })
        return results
    except Exception as e:
        print(f"[Stake {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_stake_live_odds():
    return get_stake_odds(live=True)

def get_stake_prematch_odds():
    return get_stake_odds(live=False)
