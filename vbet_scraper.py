import requests

def get_vbet_matches(live=True):
    url = "https://www.vbet.com/sportsbook/api/events/"
    url += "live" if live else "prematch"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("events", []):
            match_name = match.get("name", "Unknown Match")
            markets = match.get("markets", [])
            odds_data = []

            for market in markets:
                market_name = market.get("name", "")
                for outcome in market.get("selections", []):
                    odds_data.append({
                        "market": market_name,
                        "outcome": outcome.get("name", ""),
                        "odds": outcome.get("price", 0)
                    })

            results.append({
                "bookmaker": "VBet",
                "match": match_name,
                "match_type": "Live" if live else "Prematch",
                "odds": odds_data
            })

        return results

    except Exception as e:
        print(f"[VBET {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_vbet_live_odds():
    return get_vbet_matches(live=True)

def get_vbet_prematch_odds():
    return get_vbet_matches(live=False)
