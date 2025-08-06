import requests
from datetime import datetime

def fetch_vbet_matches(live=True):
    base_url = "https://www.vbet.com"
    endpoint = "/sportsbook/api/events/live" if live else "/sportsbook/api/events/prematch"
    
    try:
        response = requests.get(base_url + endpoint, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        matches = []
        for match in data.get("events", []):
            match_name = match.get("name", "Unknown Match")
            markets = match.get("markets", [])
            odds_data = []
            
            for market in markets:
                market_name = market.get("name", "")
                for outcome in market.get("selections", []):
                    outcome_name = outcome.get("name", "")
                    price = outcome.get("price", 0)
                    odds_data.append({
                        "market": market_name,
                        "outcome": outcome_name,
                        "odds": price
                    })

            matches.append({
                "match": match_name,
                "time": match.get("startTime", ""),
                "odds": odds_data
            })
        
        return matches

    except Exception as e:
        print(f"VBet {'Live' if live else 'Prematch'} Scraper Error:", e)
        return []

# Example usage:
if __name__ == "__main__":
    live_matches = fetch_vbet_matches(live=True)
    prematch_matches = fetch_vbet_matches(live=False)

    print("📺 LIVE MATCHES:")
    for m in live_matches[:2]:
        print(m['match'], [o['odds'] for o in m['odds'][:3]])

    print("\n⏳ PREMATCH MATCHES:")
    for m in prematch_matches[:2]:
        print(m['match'], [o['odds'] for o in m['odds'][:3]])
