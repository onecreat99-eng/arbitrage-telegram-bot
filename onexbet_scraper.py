import requests

# LIVE ODDS
def get_onexbet_live_odds():
    try:
        url = "https://1xBet.com/LiveFeed/Get1x2_VZip?lng=en&sports=1&count=50&mode=4&country=1"
        response = requests.get(url)
        data = response.json()
        results = []

        for event in data.get("Value", []):
            match = f"{event.get('O1', '')} vs {event.get('O2', '')}"
            market = "1X2"
            odds = {
                "1xBet (1)": event.get("E", [])[0].get("C", 0),
                "1xBet (X)": event.get("E", [])[1].get("C", 0),
                "1xBet (2)": event.get("E", [])[2].get("C", 0),
            }

            results.append({
                "match": match,
                "market": market,
                "odds": odds,
                "is_live": True
            })
        return results
    except Exception as e:
        print(f"[1xBet LIVE] Error: {e}")
        return []

# PREMATCH ODDS
def get_onexbet_prematch_odds():
    try:
        url = "https://1xBet.com/LineFeed/Get1x2_VZip?lng=en&sports=1&count=50&mode=4&country=1"
        response = requests.get(url)
        data = response.json()
        results = []

        for event in data.get("Value", []):
            match = f"{event.get('O1', '')} vs {event.get('O2', '')}"
            market = "1X2"
            odds = {
                "1xBet (1)": event.get("E", [])[0].get("C", 0),
                "1xBet (X)": event.get("E", [])[1].get("C", 0),
                "1xBet (2)": event.get("E", [])[2].get("C", 0),
            }

            results.append({
                "match": match,
                "market": market,
                "odds": odds,
                "is_live": False
            })
        return results
    except Exception as e:
        print(f"[1xBet PREMATCH] Error: {e}")
        return []

