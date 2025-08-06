# Trigger auto-deploy on Render
def get_arbitrage_data():
    return {
        "type": "LIVE",
        "bookmakers": [
            {"name": "1xBet", "odds": 2.1},
            {"name": "Stake", "odds": 2.2}
        ],
        "profit": 10.5,
        "match": "ABC vs XYZ",
        "market": "Fulltime Result"  # ✅ Market added here
    }

def send_alert(data):
    emojis = {
        "LIVE": "🟢",
        "PREMATCH": "🔵",
        "SAME": "🔴",
        "BOOK": "⚫",
        "PROFIT": "💰",
        "TIME": "⏰",
        "MARKET": "📊",
        "DATE": "🗓️"
    }
    time_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    message = f"{emojis[data['type']]} {data['type']} Arbitrage Found!\n"
    for bm in data['bookmakers']:
        message += f"{emojis['BOOK']} {bm['name']}: {bm['odds']}\n"
    message += f"{emojis['MARKET']} Market: {data['market']}\n"  # ✅ Add this line
    message += f"{emojis['PROFIT']} Profit: {data['profit']}%\n"
    message += f"{emojis['TIME']} Match: {data['match']}\n"
    message += f"{emojis['DATE']} {time_str}"
    bot.send_message(chat_id=CHAT_ID, text=message)
