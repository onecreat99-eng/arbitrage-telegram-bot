import requests

def get_bcgame_odds(live=True):
    url = "https://bcgame-data.example/api/live" if live else "https://bcgame-data.example/api/prematch"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("matches", []):
            results.append({
                "match": match.get("name", "Unknown Match"),
                "market": match.get("market", "Unknown Market"),
                "bookmaker": "BC.Game",
                "odds": match.get("odds", {}),
                "is_live": live
            })
        return results
    except Exception as e:
        print(f"[BC.Game {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_bcgame_live_odds():
    return get_bcgame_odds(live=True)

def get_bcgame_prematch_odds():
    return get_bcgame_odds(live=False)
