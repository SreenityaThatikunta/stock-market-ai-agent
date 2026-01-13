import requests
from config import USE_TELEGRAM, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def notify(message):
    print("\n" + "="*50)
    print(message)
    print("="*50)

    if USE_TELEGRAM and TELEGRAM_BOT_TOKEN:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, data=data)