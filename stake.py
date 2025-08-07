import requests

STAKE_API = "https://api.stake.com/sports"

def get_stake_live_odds():
    try:
        url = f"{STAKE_API}/events/live"
        r = requests.get(url, timeout=10)
        data = r.json()
        markets = []
        for event in data.get("events", []):
            match = event.get("name")
            odds = [market.get("price") for market in event.get("markets", []) if market.get("price")]
            markets.append({"match": match, "odds": odds, "type": "Live"})
        return markets
    except Exception as e:
        print(f"Stake live error: {e}")
        return []

def get_stake_prematch_odds():
    try:
        url = f"{STAKE_API}/events/upcoming"
        r = requests.get(url, timeout=10)
        data = r.json()
        markets = []
        for event in data.get("events", []):
            match = event.get("name")
            odds = [market.get("price") for market in event.get("markets", []) if market.get("price")]
            markets.append({"match": match, "odds": odds, "type": "Prematch"})
        return markets
    except Exception as e:
        print(f"Stake prematch error: {e}")
        return []
