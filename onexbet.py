import requests

def get_onexbet_odds(live=True):
    url = "https://1xbet.com/api/v1/live" if live else "https://1xbet.com/api/v1/line"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for event in data.get("events", []):
            match_name = event.get("name", "Unknown Match")
            for market in event.get("markets", []):
                odds_dict = {}
                for outcome in market.get("outcomes", []):
                    odds_dict[outcome.get("name", "Unknown")] = float(outcome.get("odds", 0))
                if odds_dict:
                    results.append({
                        "match": match_name,
                        "market": market.get("name", "Unknown Market"),
                        "bookmaker": "⚫ 1xBet",
                        "odds": odds_dict,
                        "is_live": live
                    })
        return results
    except Exception as e:
        print(f"[1xBet {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_onexbet_live_odds():
    return get_onexbet_odds(live=True)

def get_onexbet_prematch_odds():
    return get_onexbet_odds(live=False)
