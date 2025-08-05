import requests

def get_1xbet_live_odds():
    url = "https://1xbet.com/LiveFeed/Get1x2_VZip?sports=1&count=20&lng=en"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        matches = []
        for match in data["Value"]:
            team1 = match["O1"]
            team2 = match["O2"]
            odds = match["E"]
            if len(odds) >= 2:
                matches.append({
                    "team1": team1,
                    "team2": team2,
                    "odds1": odds[0]["C"],
                    "odds2": odds[1]["C"],
                })
        return matches
    except Exception as e:
        print("Scraper Error:", e)
        return []
