import requests

def get_stake_odds(live=True):
    url = "https://stake-data.example/api/live" if live else "https://stake-data.example/api/prematch"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("matches", []):
            results.append({
                "match": match.get("name", "Unknown Match"),
                "market": match.get("market", "Unknown Market"),
                "bookmaker": "Stake",
                "odds": match.get("odds", {}),
                "is_live": live,
            })
        return results
    except Exception as e:
        print(f"[Stake {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_stake_live_odds():
    return get_stake_odds(live=True)

def get_stake_prematch_odds():
    return get_stake_odds(live=False)
