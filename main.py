# Trigger auto-deploy on Render
import os
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

from 1xbet_scraper import get_onexbet_live_odds, get_onexbet_prematch_odds
from stake_scraper import get_stake_live_odds, get_stake_prematch_odds
from vbet_scraper import get_vbet_live_odds, get_vbet_prematch_odds
from bcgame_scraper import get_bcgame_live_odds, get_bcgame_prematch_odds
from mostbet_scraper import get_mostbet_live_odds, get_mostbet_prematch_odds

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Alert limit
MAX_ALERTS_PER_DAY = 8
alert_count = 0
last_reset_date = datetime.now().date()

def reset_daily_count():
    global alert_count, last_reset_date
    today = datetime.now().date()
    if today != last_reset_date:
        alert_count = 0
        last_reset_date = today

def calculate_arbitrage(odds_dict):
    try:
        inv_sum = sum(1 / max(odds.values()) for odds in odds_dict)
        profit_percent = (1 - inv_sum) * 100
        return round(profit_percent, 2)
    except:
        return -100.0

def send_alert(match, market, best_odds, profit_percent, is_live, same_bookmaker):
    global alert_count
    if alert_count >= MAX_ALERTS_PER_DAY:
        return

    time_str = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    match_type = "🟢 Live" if is_live else "🔵 Prematch"
    same_flag = "🔴 Same Bookmaker" if same_bookmaker else "⚪ Different Bookmakers"

    odds_str = "\n".join([f"⚫ {book}: {odd}" for book, odd in best_odds.items()])
    message = (
        f"{match_type} Arbitrage Alert 📢\n"
        f"📍 Match: {match}\n"
        f"📊 Market: {market}\n"
        f"{odds_str}\n"
        f"💰 Profit: {profit_percent:.2f}%\n"
        f"{same_flag}\n"
        f"🕒 {time_str}"
    )

    bot.send_message(chat_id=CHAT_ID, text=message)
    alert_count += 1

def get_all_odds():
    return (
        get_onexbet_live_odds() + get_onexbet_prematch_odds() +
        get_stake_live_odds() + get_stake_prematch_odds() +
        get_vbet_live_odds() + get_vbet_prematch_odds() +
        get_bcgame_live_odds() + get_bcgame_prematch_odds() +
        get_mostbet_live_odds() + get_mostbet_prematch_odds()
    )

def main():
    reset_daily_count()
    all_odds = get_all_odds()

    match_map = {}

    for entry in all_odds:
        match_key = (entry["match"], entry["market"])
        if match_key not in match_map:
            match_map[match_key] = []
        match_map[match_key].append(entry)

    for (match, market), entries in match_map.items():
        odds_list = [e["odds"] for e in entries]
        if len(odds_list) < 2:
            continue

        best_odds = {}
        used_books = set()

        for outcome in ["1", "X", "2"]:
            best = 0
            best_book = None
            for entry in entries:
                for book, odd in entry["odds"].items():
                    if outcome in book and odd > best:
                        best = odd
                        best_book = book
            if best_book:
                best_odds[best_book] = best
                used_books.add(best_book.split(" ")[0])  # Bookmaker name before bracket

        if len(best_odds) == 3:
            profit = calculate_arbitrage(list(best_odds.values()))
            if profit > 10:
                is_live = any(e["is_live"] for e in entries)
                same_bookmaker = len(used_books) == 1
                send_alert(match, market, best_odds, profit, is_live, same_bookmaker)

if __name__ == "__main__":
    main()
