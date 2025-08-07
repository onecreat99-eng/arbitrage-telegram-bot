import requests

BCGAME_API = "https://sports.bcgame-api.com/api/v1/events"

def get_bcgame_live_odds():
    try:
        url = f"{BCGAME_API}/live"
        r = requests.get(url, timeout=10)
        data = r.json()
        markets = []
        for event in data.get("events", []):
            match = event.get("name")
            odds = [market.get("price") for market in event.get("markets", []) if market.get("price")]
            markets.append({"match": match, "odds": odds, "type": "Live"})
        return markets
    except Exception as e:
        print(f"BC.Game live error: {e}")
        return []

def get_bcgame_prematch_odds():
    try:
        url = f"{BCGAME_API}/prematch"
        r = requests.get(url, timeout=10)
        data = r.json()
        markets = []
        for event in data.get("events", []):
            match = event.get("name")
            odds = [market.get("price") for market in event.get("markets", []) if market.get("price")]
            markets.append({"match": match, "odds": odds, "type": "Prematch"})
        return markets
    except Exception as e:
        print(f"BC.Game prematch error: {e}")
        return []
