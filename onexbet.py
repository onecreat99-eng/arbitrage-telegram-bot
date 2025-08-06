import requests

BASE_URL = "https://1xbet.com/LineFeed/Get1x2_VZip"

def get_1xbet_live_odds():
    try:
        url = f"{BASE_URL}?sports=1&count=50&lng=en&mode=4&country=1&partner=51&getEmpty=true"
        r = requests.get(url, timeout=10)
        data = r.json()
        matches = []
        for match in data.get("Value", []):
            if "O1" in match and "O2" in match:
                matches.append({
                    "bookmaker": "⚫1xBet",
                    "type": "Live",
                    "match": match.get("O1") + " vs " + match.get("O2"),
                    "market": "Fulltime Result",
                    "odds": {
                        "Home": match.get("E", [{}])[0].get("C", None),
                        "Draw": match.get("E", [{}])[1].get("C", None) if len(match.get("E", [])) > 1 else None,
                        "Away": match.get("E", [{}])[2].get("C", None) if len(match.get("E", [])) > 2 else None
                    }
                })
        return matches
    except Exception as e:
        print(f"1xBet live scrape error: {e}")
        return []

def get_1xbet_prematch_odds():
    try:
        url = f"{BASE_URL}?sports=1&count=50&lng=en&mode=4&country=1&partner=51&getEmpty=true"
        r = requests.get(url, timeout=10)
        data = r.json()
        matches = []
        for match in data.get("Value", []):
            matches.append({
                "bookmaker": "⚫1xBet",
                "type": "Prematch",
                "match": match.get("O1") + " vs " + match.get("O2"),
                "market": "Fulltime Result",
                "odds": {
                    "Home": match.get("E", [{}])[0].get("C", None),
                    "Draw": match.get("E", [{}])[1].get("C", None) if len(match.get("E", [])) > 1 else None,
                    "Away": match.get("E", [{}])[2].get("C", None) if len(match.get("E", [])) > 2 else None
                }
            })
        return matches
    except Exception as e:
        print(f"1xBet prematch scrape error: {e}")
        return []
