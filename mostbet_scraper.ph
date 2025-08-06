import requests

def get_mostbet_odds(live=True):
    url = "https://mostbet-data.example/api/live" if live else "https://mostbet-data.example/api/prematch"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("matches", []):
            results.append({
                "match": match.get("name", "Unknown Match"),
                "market": match.get("market", "Unknown Market"),
                "bookmaker": "Mostbet",
                "odds": match.get("odds", {}),
                "is_live": live,
            })
        return results
    except Exception as e:
        print(f"[Mostbet {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_mostbet_live_odds():
    return get_mostbet_odds(live=True)

def get_mostbet_prematch_odds():
    return get_mostbet_odds(live=False)
