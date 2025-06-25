import os
import requests

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return response.ok

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = "Привет! Это тестовое сообщение от бота."

    success = send_telegram_message(token, chat_id, message)
    if success:
        print("Сообщение отправлено успешно.")
    else:
        print("Ошибка при отправке сообщения.")
