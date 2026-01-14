import requests
from config import USE_TELEGRAM, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def notify(message):
    print("\n" + "="*50)
    print(message)
    print("="*50)

    print(f"[TELEGRAM DEBUG] USE_TELEGRAM={USE_TELEGRAM}, TOKEN={'set' if TELEGRAM_BOT_TOKEN else 'not set'}")

    if USE_TELEGRAM and TELEGRAM_BOT_TOKEN:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        print(f"[TELEGRAM DEBUG] Sending to chat_id: {TELEGRAM_CHAT_ID}")
        try:
            response = requests.post(url, data=data)
            print(f"[TELEGRAM DEBUG] Response status: {response.status_code}")
            print(f"[TELEGRAM DEBUG] Response body: {response.text}")
        except Exception as e:
            print(f"[TELEGRAM DEBUG] Error sending: {e}")
    else:
        print("[TELEGRAM DEBUG] Telegram disabled or token not set")