# stake_scraper.py

import requests

def get_stake_live_odds():
    return [
        {
            "match": "Stake Live Match A vs B",
            "market": "Match Winner",
            "bookmaker": "Stake",
            "odds": {"A": 2.10, "B": 1.95},
            "profit_percent": 0.0,
            "is_live": True
        }
    ]

def get_stake_prematch_odds():
    return [
        {
            "match": "Stake Pre Match C vs D",
            "market": "Match Winner",
            "bookmaker": "Stake",
            "odds": {"C": 2.20, "D": 1.80},
            "profit_percent": 0.0,
            "is_live": False
        }
    ]
