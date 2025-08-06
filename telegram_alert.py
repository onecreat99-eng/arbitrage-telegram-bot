import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_alert(arb):
    time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    alert_type = "🟢 Live" if arb["match_type"] == "Live" else "🔵 Prematch"
    same_bookmaker = "🔴 Same Bookmaker" if arb["bookmaker_1"] == arb["bookmaker_2"] else "⚪ Different Bookmakers"

    message = f"""
🔥 *Arbitrage Opportunity Found* 🔥

🏟️ *Match:* {arb['match']}
🎯 *Market:* {arb['market']}

⚫ {arb['bookmaker_1']} ➤ {arb['outcome_1']} @ {arb['odds_1']}
⚫ {arb['bookmaker_2']} ➤ {arb['outcome_2']} @ {arb['odds_2']}

💰 *Profit:* {arb['profit_percent']}%
{alert_type} | {same_bookmaker}
🕒 {time_now}
""".strip()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)
