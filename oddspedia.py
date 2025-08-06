import requests
from bs4 import BeautifulSoup

def get_oddspedia_odds():
    url = "https://oddspedia.com/football"  # Example: Football section
    headers = {"User-Agent": "Mozilla/5.0"}

    results = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        matches = soup.select(".eventRow")
        for match in matches:
            match_name = match.select_one(".eventCell--name").get_text(strip=True)
            match_type = "Live" if match.select_one(".liveNow") else "Prematch"
            market = "Fulltime Result"

            bookmaker_cells = match.select(".bookmakerCell")
            for book in bookmaker_cells:
                book_name = book.get("data-bk", "").lower()
                if book_name in ["1xbet", "bc.game"]:
                    odds_dict = {}
                    odds_values = book.select(".odd")
                    teams = match.select(".participant__participantName")
                    if len(teams) == len(odds_values):
                        for i, team in enumerate(teams):
                            try:
                                odds_dict[team.get_text(strip=True)] = float(odds_values[i].get_text(strip=True))
                            except:
                                continue
                        results.append({
                            "match": match_name,
                            "market": market,
                            "bookmaker": book_name.capitalize(),
                            "odds": odds_dict,
                            "type": match_type
                        })
        return results
    except Exception as e:
        print("Oddspedia Error:", e)
        return []
