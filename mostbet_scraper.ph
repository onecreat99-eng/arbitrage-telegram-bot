import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://mostbet.com"

def get_mostbet_odds(url, match_type):
    odds_data = []
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        matches = soup.select(".event-card")
        for match in matches:
            teams = match.select_one(".event-card__name").get_text(strip=True)
            odds = match.select(".bet-button__odds")
            if len(odds) >= 2:
                odds_data.append({
                    "match": teams,
                    "bookmaker": "Mostbet",
                    "type": match_type,
                    "odds": {
                        "home": float(odds[0].get_text(strip=True)),
                        "away": float(odds[1].get_text(strip=True))
                    },
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    except Exception as e:
        print(f"Mostbet {match_type} scrape error: {e}")
    return odds_data

def get_mostbet_live_odds():
    url = f"{BASE_URL}/sports/live"
    return get_mostbet_odds(url, "Live")

def get_mostbet_prematch_odds():
    url = f"{BASE_URL}/sports/"
    return get_mostbet_odds(url, "Prematch")
