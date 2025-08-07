import requests

BASE_URL = "https://1xbet.com/LineFeed/Get1x2_VZip"

def get_1xbet_live_odds():
    try:
        url = f"{BASE_URL}?sports=0&count=20&lng=en&mode=4"
        r = requests.get(url, timeout=10)
        data = r.json()
        markets = []
        for event in data.get("Value", []):
            match = event.get("O1") + " vs " + event.get("O2")
            odds = [sel.get("C") for sel in event.get("E", [])]
            markets.append({"match": match, "odds": odds, "type": "Live"})
        return markets
    except Exception as e:
        print(f"1xBet live error: {e}")
        return []

def get_1xbet_prematch_odds():
    try:
        url = f"{BASE_URL}?sports=0&count=20&lng=en&mode=1"
        r = requests.get(url, timeout=10)
        data = r.json()
        markets = []
        for event in data.get("Value", []):
            match = event.get("O1") + " vs " + event.get("O2")
            odds = [sel.get("C") for sel in event.get("E", [])]
            markets.append({"match": match, "odds": odds, "type": "Prematch"})
        return markets
    except Exception as e:
        print(f"1xBet prematch error: {e}")
        return []
