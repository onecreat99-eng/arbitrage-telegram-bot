import requests

BCGAME_API = "https://sports.bcgame.com/api/sports"

def fetch_bcgame_data():
    try:
        res = requests.get(BCGAME_API, timeout=10)
        res.raise_for_status()
        data = res.json()
        results = []

        for match in data.get("matches", []):
            match_name = match.get("home", "") + " vs " + match.get("away", "")
            for market in match.get("markets", []):
                odds = {}
                for outcome in market.get("selections", []):
                    odds[outcome.get("name", "")] = outcome.get("odds", None)

                results.append({
                    "match": match_name.strip(),
                    "market": market.get("name", "Unknown Market"),
                    "bookmaker": "⚫ BC.Game",
                    "odds": odds,
                    "is_live": match.get("live", False)
                })
        return results
    except Exception as e:
        print("[BC.Game] Error:", e)
        return []

def get_bcgame_live_odds():
    return fetch_bcgame_data()

def get_bcgame_prematch_odds():
    return fetch_bcgame_data()
