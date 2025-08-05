# Trigger auto-deploy on Render
import time
from onexbet_live_scraper import get_1xbet_live_odds
from telegram import Bot
from datetime import datetime

# Telegram setup
BOT_TOKEN = "your_telegram_bot_token"
CHAT_ID = "your_chat_id"
bot = Bot(token=BOT_TOKEN)

sent_alerts = set()

while True:
    try:
        matches = get_1xbet_live_odds()

        for match in matches:
            team1 = match['team1']
            team2 = match['team2']
            odds = match['odds']
            match_name = f"{team1} vs {team2}"
            key = match_name + str(odds)

            if key in sent_alerts:
                continue

            # Dummy logic: if odds 1 and 2 are high enough
            if odds['1'] > 2.0 and odds['2'] > 2.0:
                profit_percent = round((1 / odds['1'] + 1 / odds['2']) * 100, 2)
                alert = (
                    f"🟢 LIVE Arbitrage Found!\n"
                    f"⚫1xBet: {odds['1']}\n"
                    f"⚫Stake: {odds['2']}\n"
                    f"💰Profit: {100 - profit_percent:.1f}%\n"
                    f"⏰Match: {match_name}\n"
                    f"📅 {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
                )
                bot.send_message(chat_id=CHAT_ID, text=alert)
                sent_alerts.add(key)

        time.sleep(30)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
