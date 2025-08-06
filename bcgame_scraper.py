import requests

def fetch_bcgame_data(endpoint, live):
    try:
        res = requests.get(endpoint, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        res.raise_for_status()
        data = res.json()

        results = []
        for match in data.get("data", []):
            teams = match.get("teams", [])
            if len(teams) < 2:
                continue

            for market in match.get("markets", []):
                market_name = market.get("name") or market.get("key")
                odds_dict = {}

                for outcome in market.get("outcomes", []):
                    label = outcome.get("label")
                    odds_value = outcome.get("odds")
                    if label and odds_value:
                        try:
                            odds_dict[label] = float(odds_value)
                        except:
                            continue

                if odds_dict:
                    results.append({
                        "match": f"{teams[0]} vs {teams[1]}",
                        "market": market_name,
                        "bookmaker": "⚫ BC.Game",
                        "odds": odds_dict,
                        "is_live": live
                    })

        return results

    except Exception as e:
        print(f"[BC.Game {'LIVE' if live else 'PREMATCH'}] Error:", e)
        return []


def get_bcgame_live_odds():
    # Live sports ka endpoint
    endpoint = "https://sports.bc.game/api/sports/live"
    return fetch_bcgame_data(endpoint, live=True)

def get_bcgame_prematch_odds():
    # Prematch sports ka endpoint
    endpoint = "https://sports.bc.game/api/sports/pre-match"
    return fetch_bcgame_data(endpoint, live=False)
