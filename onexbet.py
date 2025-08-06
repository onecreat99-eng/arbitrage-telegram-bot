import requests

BASE_URL = "https://1xbet.com/LineFeed/Get1x2_VZip"

def get_1xbet_live_odds():
    """
    1xBet से live odds fetch करता है।
    """
    params = {
        "sports": 0,        # All sports
        "count": 50,        # कितने matches चाहिए
        "lng": "en",
        "mode": 4,          # Live mode
        "country": 1,
        "partner": 51
    }
    try:
        res = requests.get(BASE_URL, params=params, timeout=10)
        data = res.json()
        matches = data.get("Value", [])
        return matches
    except Exception as e:
        print(f"1xBet Live Odds Error: {e}")
        return []

def get_1xbet_prematch_odds():
    """
    1xBet से prematch odds fetch करता है।
    """
    params = {
        "sports": 0,
        "count": 50,
        "lng": "en",
        "mode": 1,         # Prematch mode
        "country": 1,
        "partner": 51
    }
    try:
        res = requests.get(BASE_URL, params=params, timeout=10)
        data = res.json()
        matches = data.get("Value", [])
        return matches
    except Exception as e:
        print(f"1xBet Prematch Odds Error: {e}")
        return []
