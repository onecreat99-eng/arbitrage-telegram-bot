import requests

def get_bcgame_odds(live=True):
    url = "https://sports.bc.game/api/v1/events/live" if live else "https://sports.bc.game/api/v1/events/upcoming"
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        results = []
        for match in data.get("data", []):
            odds_dict = {}
            for market in match.get("markets", []):
                if market.get("key") == "match_winner":
                    for outcome in market.get("outcomes", []):
                        odds_dict[outcome.get("name", "")] = outcome.get("price", 0)
            
            if odds_dict:
                results.append({
                    "match": match.get("home_team", "") + " vs " + match.get("away_team", ""),
                    "market": "Match Winner",
                    "bookmaker": "BC.Game",
                    "odds": odds_dict,
                    "is_live": live
                })
        return results
    except Exception as e:
        print(f"[BC.GAME {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []

def get_bcgame_live_odds():
    return get_bcgame_odds(live=True)

def get_bcgame_prematch_odds():
    return get_bcgame_odds(live=False)
