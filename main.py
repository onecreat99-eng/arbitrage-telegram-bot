# Trigger auto-deploy on Render
for arb in arbitrage_data:
    team1 = arb.get("team1", "Team A")
    team2 = arb.get("team2", "Team B")
    match_name = f"{team1} vs {team2}"  # ✅ Now dynamic!

    market = arb["market"]
    bookmaker_1 = arb["bookmaker_1"]
    bookmaker_2 = arb["bookmaker_2"]
    odds_1 = arb["odds_1"]
    odds_2 = arb["odds_2"]
    match_type = arb["match_type"]
    profit = arb["profit"]

    # Emoji logic
    emoji = "🟢" if match_type.lower() == "live" else "🔵"
    type_emoji = "🟡"

    # Time formatting
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    time_str = now.strftime("%H:%M:%S | %d-%m-%Y")

    # Telegram message
    message = f"""
{emoji} *{match_type} Arbitrage Alert!*

*Match:* {match_name}
*Market:* {market}
*Odds:* ⚫ {bookmaker_1} @ {odds_1} vs ⚫ {bookmaker_2} @ {odds_2}
*Profit:* {profit:.2f}%
*Type:* {type_emoji} Cross Bookmaker
*Time:* {time_str}
"""

    # Send to Telegram
    send_telegram_message(message.strip())
