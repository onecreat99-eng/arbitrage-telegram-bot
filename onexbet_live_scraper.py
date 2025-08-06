import requests

def get_onexbet_live_odds():
    return [
        {
            "match": "1xBet Live Match A vs B",
            "market": "Match Winner",
            "bookmaker": "1xBet",
            "odds": {"A": 2.00, "B": 1.90},
            "profit_percent": 0.0,
            "is_live": True
        }
    ]

def get_onexbet_prematch_odds():
    return [
        {
            "match": "1xBet Prematch C vs D",
            "market": "Match Winner",
            "bookmaker": "1xBet",
            "odds": {"C": 2.15, "D": 1.85},
            "profit_percent": 0.0,
            "is_live": False
        }
    ]

