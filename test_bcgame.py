from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds

print("📢 Fetching BC.Game LIVE odds...")
live_data = get_bcgame_live_odds()
print(f"✅ Total live records: {len(live_data)}")
if live_data:
    print(live_data[:3])  # sirf pehle 3 matches dikhayega

print("\n📢 Fetching BC.Game PREMATCH odds...")
prematch_data = get_bcgame_prematch_odds()
print(f"✅ Total prematch records: {len(prematch_data)}")
if prematch_data:
    print(prematch_data[:3])
