# Trigger auto-deploy on Render
from datetime import datetime

def send_alert(match, bookmaker1, odds1, bookmaker2, odds2, profit_percent, match_type, bot, chat_id):
    now = datetime.now().strftime('%I:%M %p')

    # 🟢 or 🔵 based on match type
    if match_type.lower() == "live":
        match_type_emoji = "🟢 LIVE Arbitrage Found!"
    else:
        match_type_emoji = "🔵 PREMATCH Arbitrage Found!"

    message = (
        f"{match_type_emoji}\n"
        f"⚫ {bookmaker1}: {odds1}\n"
        f"⚫ {bookmaker2}: {odds2}\n"
        f"💰 Profit: {profit_percent:.1f}%\n"
        f"⏰ Match: {match}\n"
        f"🕒 {now}"
    )

    bot.send_message(chat_id=chat_id, text=message)
