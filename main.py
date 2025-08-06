# Trigger auto-deploy on Render
import os
from flask import Flask
import threading
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Flask server setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Arbitrage Bot is running!"

def run_server():
    app.run(host="0.0.0.0", port=10000)

# Function to send Telegram message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

# Dummy function for scraping data
def scrape_arbitrage():
    # यहाँ पर अपना real scraping code डालो
    print("Scraping arbitrage data...")
    # Example alert
    send_telegram_message("✅ Arbitrage Opportunity Found! (Example)")

# Main loop
def main():
    while True:
        scrape_arbitrage()
        time.sleep(300)  # हर 5 मिनट में चलाओ

if __name__ == "__main__":
    # Flask server को अलग thread में चलाओ
    threading.Thread(target=run_server).start()
    # Bot main function
    main()
