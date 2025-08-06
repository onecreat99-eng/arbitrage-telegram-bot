import requests

BASE_URL = "https://sports.bcgame.com/api/v1/betline/events"

def get_bcgame_odds():
    """
    Scrapes BC.Game odds for all sports, all markets, live & prematch
    Returns: list of dict with match, market, bookmaker, odds, is_live
    """
    results = []

    try:
        # Fetch data for both LIVE and PREMATCH
        for status in ["LIVE", "PREMATCH"]:
            params = {
                "limit": 50,       # number of events
                "status": status   # LIVE or PREMATCH
            }
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            for event in data.get("data", []):
                match_name = f"{event['home']['name']} vs {event['away']['name']}"
                is_live = (status == "LIVE")

                for market in event.get("markets", []):
                    market_name = market.get("key", "Unknown Market")
                    odds_data = {}
                    for outcome in market.get("outcomes", []):
                        odds_data[outcome["name"]] = outcome["odds"]

                    results.append({
                        "match": match_name,
                        "market": market_name,
                        "bookmaker": "⚫ BC.Game",
                        "odds": odds_data,
                        "is_live": is_live
                    })

    except Exception as e:
        print(f"BC.Game scraping error: {e}")

    return results
