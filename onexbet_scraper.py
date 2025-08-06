import requests

def get_onexbet_odds(live=True):
    url = "https://1xbet.com/LiveFeed/Get1x2" if live else "https://1xbet.com/LiveFeed/Get1x2Prematch"
    params = {"sportId": 1, "lng": "en"}
    
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        results = []
        for match in data.get("Value", []):
            results.append({
                "match": match.get("O1", "") + " vs " + match.get("O2", ""),
                "market": "Match Winner",
                "bookmaker": "1xBet",
                "odds": {
                    match.get("O1", ""): match.get("P1", 0),
                    match.get("O2", ""): match.get("P2", 0)
                },
                "is_live": live
            })
        return results
    except Exception as e:
        print(f"[1XBET {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_onexbet_live_odds():
    return get_onexbet_odds(live=True)

def get_onexbet_prematch_odds():
    return get_onexbet_odds(live=False)
