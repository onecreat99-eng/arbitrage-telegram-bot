import requests

def get_mostbet_odds(live=True):
    url = "https://mostbet.com/api/v1/sports/live" if live else "https://mostbet.com/api/v1/sports/prematch"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("matches", []):
            results.append({
                "match": match.get("homeTeam", "") + " vs " + match.get("awayTeam", ""),
                "market": "Match Winner",
                "bookmaker": "⚫ Mostbet",
                "odds": {
                    match.get("homeTeam", ""): match.get("markets", [{}])[0].get("outcomes", [{}])[0].get("odds", 0),
                    match.get("awayTeam", ""): match.get("markets", [{}])[0].get("outcomes", [{}])[1].get("odds", 0)
                },
                "is_live": live
            })
        return results
    except Exception as e:
        print(f"[Mostbet {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_mostbet_live_odds():
    return get_mostbet_odds(live=True)

def get_mostbet_prematch_odds():
    return get_mostbet_odds(live=False)
