import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MESSAGE = "✅ Test message from GitHub Actions!"

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing.")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": MESSAGE}

response = requests.post(url, data=data)

if response.status_code == 200:
    print("✅ Message sent successfully!")
else:
    print(f"❌ Failed to send message. Response: {response.text}")
