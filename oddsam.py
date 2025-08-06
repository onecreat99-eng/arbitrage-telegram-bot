import requests
from bs4 import BeautifulSoup

def get_oddsam_odds():
    url = "https://odds.am/en/odds/"
    headers = {"User-Agent": "Mozilla/5.0"}

    results = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        matches = soup.select(".match-row")
        for match in matches:
            match_name = match.select_one(".match-name").get_text(strip=True)
            match_type = "Live" if match.select_one(".live-label") else "Prematch"
            market = "Fulltime Result"

            bookmakers = match.select(".bookmaker-odds")
            for book in bookmakers:
                book_name = book.get("data-bookmaker", "").lower()
                if book_name in ["1xbet", "bc.game"]:
                    odds_dict = {}
                    odds_cells = book.select(".odds-cell")
                    teams = match.select(".participant")
                    if len(teams) == len(odds_cells):
                        for i, team in enumerate(teams):
                            try:
                                odds_dict[team.get_text(strip=True)] = float(odds_cells[i].get_text(strip=True))
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
        print("Odds.am Error:", e)
        return []
