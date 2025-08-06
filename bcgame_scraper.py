import requests

def get_bcgame_odds(live=True):
    url = "https://sports-api.bcgame.bio/api/v1/public/sports"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for sport in data.get("data", []):
            for match in sport.get("matches", []):
                results.append({
                    "match": match.get("homeTeam", "") + " vs " + match.get("awayTeam", ""),
                    "market": "Match Winner",
                    "bookmaker": "⚫ BC.Game",
                    "odds": {
                        match.get("homeTeam", ""): match.get("markets", [{}])[0].get("outcomes", [{}])[0].get("odds", 0),
                        match.get("awayTeam", ""): match.get("markets", [{}])[0].get("outcomes", [{}])[1].get("odds", 0)
                    },
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
