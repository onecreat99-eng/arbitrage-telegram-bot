import requests

def get_bcgame_odds():
    results = []

    try:
        # Live odds
        live_url = "https://bc.game/api/sports/live"
        live_data = requests.get(live_url, timeout=10).json()
        for match in live_data.get("data", []):
            results.append({
                "bookmaker": "BC.Game",
                "type": "Live",
                "match": match.get("home") + " vs " + match.get("away"),
                "market": "Fulltime Result",
                "odds": [
                    match["markets"][0]["selections"][0]["odds"],
                    match["markets"][0]["selections"][1]["odds"],
                    match["markets"][0]["selections"][2]["odds"]
                ]
            })

        # Prematch odds
        pre_url = "https://bc.game/api/sports/upcoming"
        pre_data = requests.get(pre_url, timeout=10).json()
        for match in pre_data.get("data", []):
            results.append({
                "bookmaker": "BC.Game",
                "type": "Prematch",
                "match": match.get("home") + " vs " + match.get("away"),
                "market": "Fulltime Result",
                "odds": [
                    match["markets"][0]["selections"][0]["odds"],
                    match["markets"][0]["selections"][1]["odds"],
                    match["markets"][0]["selections"][2]["odds"]
                ]
            })

    except Exception as e:
        print(f"[BC.Game ERROR] {e}")

    return results
