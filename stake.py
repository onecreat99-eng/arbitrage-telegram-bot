import requests

def get_stake_odds():
    results = []

    try:
        # Live odds
        live_url = "https://stake.com/api/sports/live"
        live_data = requests.get(live_url, timeout=10).json()
        for sport in live_data.get("sports", []):
            for match in sport.get("events", []):
                results.append({
                    "bookmaker": "Stake",
                    "type": "Live",
                    "match": match.get("home") + " vs " + match.get("away"),
                    "market": "Fulltime Result",
                    "odds": [
                        match["markets"][0]["selections"][0]["price"],
                        match["markets"][0]["selections"][1]["price"],
                        match["markets"][0]["selections"][2]["price"]
                    ]
                })

        # Prematch odds
        pre_url = "https://stake.com/api/sports/upcoming"
        pre_data = requests.get(pre_url, timeout=10).json()
        for sport in pre_data.get("sports", []):
            for match in sport.get("events", []):
                results.append({
                    "bookmaker": "Stake",
                    "type": "Prematch",
                    "match": match.get("home") + " vs " + match.get("away"),
                    "market": "Fulltime Result",
                    "odds": [
                        match["markets"][0]["selections"][0]["price"],
                        match["markets"][0]["selections"][1]["price"],
                        match["markets"][0]["selections"][2]["price"]
                    ]
                })

    except Exception as e:
        print(f"[Stake ERROR] {e}")

    return results
