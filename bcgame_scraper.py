import requests

def get_bcgame_live_odds():
    return [
        {
            "match": "BC.Game Live Match P vs Q",
            "market": "Match Winner",
            "bookmaker": "BC.Game",
            "odds": {"P": 2.00, "Q": 1.98},
            "profit_percent": 0.0,
            "is_live": True
        }
    ]

def get_bcgame_prematch_odds():
    return [
        {
            "match": "BC.Game Prematch E vs F",
            "market": "Match Winner",
            "bookmaker": "BC.Game",
            "odds": {"E": 2.15, "F": 1.85},
            "profit_percent": 0.0,
            "is_live": False
        }
    ]
