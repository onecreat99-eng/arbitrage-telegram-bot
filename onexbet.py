import requests

BASE_URL = "https://1xbet.com/LineFeed"

def fetch_1xbet_data(endpoint):
    try:
        res = requests.get(endpoint, timeout=10)
        res.raise_for_status()
        data = res.json()
        results = []

        for match in data.get("Value", []):
            match_name = match.get("O1", "") + " vs " + match.get("O2", "")
            markets = match.get("Markets", [])

            for market in markets:
                odds = {}
                for outcome in market.get("E", []):
                    odds[outcome.get("O", "")] = outcome.get("C", None)

                results.append({
                    "match": match_name.strip(),
                    "market": market.get("T", "Unknown Market"),
                    "bookmaker": "⚫ 1xBet",
                    "odds": odds,
                    "is_live": match.get("IsLive", False)
                })
        return results
    except Exception as e:
        print("[1xBet] Error:", e)
        return []

def get_1xbet_live_odds():
    url = f"{BASE_URL}/Get1x2_VZip?sports=0&count=50&mode=4&country=1&partner=1&getEmpty=true&virtualSports=true"
    return fetch_1xbet_data(url)

def get_1xbet_prematch_odds():
    url = f"{BASE_URL}/Get1x2_VZip?sports=0&count=50&mode=4&country=1&partner=1&getEmpty=true&virtualSports=true"
    return fetch_1xbet_data(url)
