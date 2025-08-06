import requests

def get_onexbet_odds():
    results = []

    try:
        # Live odds
        live_url = "https://1xbet.com/LiveFeed/Get1x2?sports=0&count=50&lng=en&mode=4"
        live_data = requests.get(live_url, timeout=10).json()
        for match in live_data.get("Value", []):
            results.append({
                "bookmaker": "1xBet",
                "type": "Live",
                "match": match.get("O1") + " vs " + match.get("O2"),
                "market": "Fulltime Result",
                "odds": [
                    match.get("E")[0]["C"],  # Home
                    match.get("E")[1]["C"],  # Draw
                    match.get("E")[2]["C"]   # Away
                ]
            })

        # Prematch odds
        pre_url = "https://1xbet.com/LineFeed/Get1x2?sports=0&count=50&lng=en&mode=4"
        pre_data = requests.get(pre_url, timeout=10).json()
        for match in pre_data.get("Value", []):
            results.append({
                "bookmaker": "1xBet",
                "type": "Prematch",
                "match": match.get("O1") + " vs " + match.get("O2"),
                "market": "Fulltime Result",
                "odds": [
                    match.get("E")[0]["C"],
                    match.get("E")[1]["C"],
                    match.get("E")[2]["C"]
                ]
            })

    except Exception as e:
        print(f"[1xBet ERROR] {e}")

    return results
