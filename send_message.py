import os
import requests

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(url, data=payload)
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        
        if response.status_code != 200:
            print("Ошибка при отправке сообщения.")
            return False
        else:
            print("Сообщение успешно отправлено.")
            return True
    except Exception as e:
        print("Ошибка при запросе:", e)
        return False

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        print("Ошибка: переменная TELEGRAM_TOKEN не задана.")
    elif not chat_id:
        print("Ошибка: переменная TELEGRAM_CHAT_ID не задана.")
    else:
        message = "✅ Привет! Это сообщение от GitHub Actions-бота."
        send_telegram_message(token, chat_id, message)
