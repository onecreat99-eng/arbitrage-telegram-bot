import requests

def get_1xbet_live_odds():
    try:
        url = "https://1xbet-data.example/api/live"
        data = requests.get(url).json()
        return [{"match": m["name"], "market": m["market"], "odds": float(m["odds"])} for m in data]
    except:
        return []

def get_1xbet_prematch_odds():
    try:
        url = "https://1xbet-data.example/api/prematch"
        data = requests.get(url).json()
        return [{"match": m["name"], "market": m["market"], "odds": float(m["odds"])} for m in data]
    except:
        return []
