import requests

BCGAME_API_URL = "https://sports.bc.game/api/v1/events"

def get_bcgame_live_odds():
    try:
        r = requests.get(f"{BCGAME_API_URL}?status=live", timeout=10)
        data = r.json()
        matches = []
        for match in data.get("data", []):
            if "markets" in match:
                for market in match["markets"]:
                    if market.get("key") == "match-winner":
                        outcomes = market.get("selections", [])
                        matches.append({
                            "bookmaker": "⚫BC.Game",
                            "type": "Live",
                            "match": match.get("homeTeam") + " vs " + match.get("awayTeam"),
                            "market": "Fulltime Result",
                            "odds": {
                                "Home": outcomes[0].get("odds") if len(outcomes) > 0 else None,
                                "Draw": outcomes[1].get("odds") if len(outcomes) > 2 else None,
                                "Away": outcomes[-1].get("odds") if len(outcomes) > 1 else None
                            }
                        })
        return matches
    except Exception as e:
        print(f"BC.Game live scrape error: {e}")
        return []

def get_bcgame_prematch_odds():
    try:
        r = requests.get(f"{BCGAME_API_URL}?status=upcoming", timeout=10)
        data = r.json()
        matches = []
        for match in data.get("data", []):
            if "markets" in match:
                for market in match["markets"]:
                    if market.get("key") == "match-winner":
                        outcomes = market.get("selections", [])
                        matches.append({
                            "bookmaker": "⚫BC.Game",
                            "type": "Prematch",
                            "match": match.get("homeTeam") + " vs " + match.get("awayTeam"),
                            "market": "Fulltime Result",
                            "odds": {
                                "Home": outcomes[0].get("odds") if len(outcomes) > 0 else None,
                                "Draw": outcomes[1].get("odds") if len(outcomes) > 2 else None,
                                "Away": outcomes[-1].get("odds") if len(outcomes) > 1 else None
                            }
                        })
        return matches
    except Exception as e:
        print(f"BC.Game prematch scrape error: {e}")
        return []
