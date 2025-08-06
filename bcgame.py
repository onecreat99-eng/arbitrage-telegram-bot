import requests

def get_bcgame_odds(live=True):
    url = "https://sports.bc.game/api/v1/events/ongoing" if live else "https://sports.bc.game/api/v1/events/upcoming"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        for event in data.get("data", []):
            match_name = f"{event.get('home_team', 'Unknown')} vs {event.get('away_team', 'Unknown')}"
            for market in event.get("markets", []):
                odds_dict = {}
                for outcome in market.get("outcomes", []):
                    odds_dict[outcome.get("label", "Unknown")] = float(outcome.get("odds", 0))
                if odds_dict:
                    results.append({
                        "match": match_name,
                        "market": market.get("name", "Unknown Market"),
                        "bookmaker": "⚫ BC.Game",
                        "odds": odds_dict,
                        "is_live": live
                    })
        return results
    except Exception as e:
        print(f"[BC.Game {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_bcgame_live_odds():
    return get_bcgame_odds(live=True)

def get_bcgame_prematch_odds():
    return get_bcgame_odds(live=False)
