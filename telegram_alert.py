# telegram_alert.py

import requests
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_alert(message):
    time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    final_message = f"{message}\n🕒 {time_now}"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": final_message
    }
    
    response = requests.post(url, data=data)
    return response.status_code
