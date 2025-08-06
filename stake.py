import requests

STAKE_API_URL = "https://stake.com/_api/sports/live/events"

def get_stake_live_odds():
    try:
        r = requests.get(STAKE_API_URL, timeout=10)
        data = r.json()
        matches = []
        for match in data.get("events", []):
            if "markets" in match:
                for market in match["markets"]:
                    if market.get("key") == "match-winner":
                        outcomes = market.get("selections", [])
                        matches.append({
                            "bookmaker": "⚫Stake",
                            "type": "Live",
                            "match": match.get("name"),
                            "market": "Fulltime Result",
                            "odds": {
                                "Home": outcomes[0].get("price") if len(outcomes) > 0 else None,
                                "Draw": outcomes[1].get("price") if len(outcomes) > 2 else None,
                                "Away": outcomes[-1].get("price") if len(outcomes) > 1 else None
                            }
                        })
        return matches
    except Exception as e:
        print(f"Stake live scrape error: {e}")
        return []

def get_stake_prematch_odds():
    try:
        r = requests.get("https://stake.com/_api/sports/upcoming/events", timeout=10)
        data = r.json()
        matches = []
        for match in data.get("events", []):
            if "markets" in match:
                for market in match["markets"]:
                    if market.get("key") == "match-winner":
                        outcomes = market.get("selections", [])
                        matches.append({
                            "bookmaker": "⚫Stake",
                            "type": "Prematch",
                            "match": match.get("name"),
                            "market": "Fulltime Result",
                            "odds": {
                                "Home": outcomes[0].get("price") if len(outcomes) > 0 else None,
                                "Draw": outcomes[1].get("price") if len(outcomes) > 2 else None,
                                "Away": outcomes[-1].get("price") if len(outcomes) > 1 else None
                            }
                        })
        return matches
    except Exception as e:
        print(f"Stake prematch scrape error: {e}")
        return []
