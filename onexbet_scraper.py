import requests

def get_onexbet_matches(live=True):
    url = "https://1xbet.com/live" if live else "https://1xbet.com/prematch"
    # This is just placeholder. Replace with real endpoint or scraping logic
    return []

def get_onexbet_live_odds():
    return get_onexbet_matches(live=True)

def get_onexbet_prematch_odds():
    return get_onexbet_matches(live=False)
