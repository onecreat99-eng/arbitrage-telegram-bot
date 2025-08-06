import requests

def get_oddsam_odds(bookmakers=('1xbet','bc.game')):
    url = "https://api.odds.am/v3/offer/surebets"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    results = []
    for arb in data:
        bm1 = arb.get("bk1")
        bm2 = arb.get("bk2")
        if bm1 in bookmakers or bm2 in bookmakers:
            results.append({
                "match": arb.get("event"),
                "market": arb.get("market"),
                "bookmaker1": bm1,
                "odds1": float(arb.get("o1")),
                "bookmaker2": bm2,
                "odds2": float(arb.get("o2")),
                "profit": float(arb.get("profit")),
                "is_live": arb.get("live") == 1
            })
    return results
