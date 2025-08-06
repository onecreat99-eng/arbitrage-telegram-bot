import requests

def get_vbet_matches(live=True):
    url = "https://www.vbet.com/sportsbook/api/events/"
    url += "live" if live else "prematch"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("events", []):
            match_name = match.get("name", "Unknown Match")
            markets = match.get("markets", [])
            odds = {}

            for market in markets:
                market_name = market.get("name", "")
                for outcome in market.get("selections", []):
                    key = f"{market_name} - {outcome.get('name', '')}"
                    odds["VBet"] = outcome.get("price", 0)

            if odds:
                results.append({
                    "bookmaker": "VBet",
                    "match": match_name,
                    "market": market_name,
                    "odds": odds,
                    "is_live": live
                })

        return results

    except Exception as e:
        print(f"[VBET {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_vbet_live_odds():
    return get_vbet_matches(live=True)

def get_vbet_prematch_odds():
    return get_vbet_matches(live=False)
