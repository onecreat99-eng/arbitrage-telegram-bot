import requests

def get_mostbet_live_odds():
    return [
        {
            "match": "Mostbet Live Match X vs Y",
            "market": "Match Winner",
            "bookmaker": "Mostbet",
            "odds": {"X": 2.05, "Y": 1.95},
            "profit_percent": 0.0,
            "is_live": True
        }
    ]

def get_mostbet_prematch_odds():
    return [
        {
            "match": "Mostbet Prematch M vs N",
            "market": "Match Winner",
            "bookmaker": "Mostbet",
            "odds": {"M": 2.10, "N": 1.90},
            "profit_percent": 0.0,
            "is_live": False
        }
    ]
