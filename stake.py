import requests

STAKE_API = "https://api.stake.com/sports/all/matches"

def fetch_stake_data():
    try:
        res = requests.get(STAKE_API, timeout=10)
        res.raise_for_status()
        data = res.json()
        results = []

        for match in data.get("matches", []):
            match_name = match.get("home_team", "") + " vs " + match.get("away_team", "")
            for market in match.get("markets", []):
                odds = {}
                for outcome in market.get("outcomes", []):
                    odds[outcome.get("name", "")] = outcome.get("price", None)

                results.append({
                    "match": match_name.strip(),
                    "market": market.get("key", "Unknown Market"),
                    "bookmaker": "⚫ Stake",
                    "odds": odds,
                    "is_live": match.get("live", False)
                })
        return results
    except Exception as e:
        print("[Stake] Error:", e)
        return []

def get_stake_live_odds():
    return fetch_stake_data()

def get_stake_prematch_odds():
    return fetch_stake_data()
