import requests

def get_1xbet_odds(live=True):
    url = "https://1xbet-data.example/api/live" if live else "https://1xbet-data.example/api/prematch"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("matches", []):
            results.append({
                "match": match.get("name", "Unknown Match"),
                "market": match.get("market", "Unknown Market"),
                "bookmaker": "1xBet",
                "odds": match.get("odds", {}),
                "is_live": live,
            })
        return results
    except Exception as e:
        print(f"[1xBet {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_1xbet_live_odds():
    return get_1xbet_odds(live=True)

def get_1xbet_prematch_odds():
    return get_1xbet_odds(live=False)
