import requests
from bs4 import BeautifulSoup

def get_vbet_matches():
    url = "https://www.vbet.com/en/sports"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        for event in soup.select(".sports-events-list-item"):
            match_name = event.get_text(strip=True)
            matches.append({"match": match_name})

        return matches

    except Exception as e:
        print("VBet Scraper Error:", e)
        return []

if __name__ == "__main__":
    data = get_vbet_matches()
    for match in data[:5]:
        print("🎯 Match:", match["match"])
