import requests

# ⛔ IMPORTANT: Yeh values apne new token & chat ID se replace karo
TOKEN = "7668611215:AAFL9nXg8E9i09VC1r1i7k4gpbybrmI88dQ"
CHAT_ID = "7244013092"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(response.text)

# ✅ Test message
send_telegram_message("✅ Bot is working and connected to Telegram!")
