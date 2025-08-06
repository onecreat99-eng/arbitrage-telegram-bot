import os
import requests

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = "straightforward_understanding/oddspedia-surebet-actor"

def get_oddspedia_surebets():
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}&limit=1"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    run_id = data["data"][0]["id"]
    result_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs/{run_id}/dataset/items?token={APIFY_TOKEN}"
    resp2 = requests.get(result_url, timeout=10)
    resp2.raise_for_status()
    items = resp2.json()
    results = []
    for item in items:
        results.append({
            "match": item.get("event"),
            "market": item.get("market"),
            "bookmaker": item.get("bookmaker"),
            "odds": item.get("decimal"),
            "is_live": item.get("type") == "live"
        })
    return results
