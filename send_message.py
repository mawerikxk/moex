import os
import requests

def get_price(ticker):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
    try:
        response = requests.get(url)
        data = response.json()
        secdata = data['marketdata']['data']
        columns = data['marketdata']['columns']
        
        if not secdata:
            return f"{ticker} — нет данных"
        
        last_index = columns.index("LAST")
        last_price = secdata[0][last_index]
        return f"{ticker} — {last_price} ₽" if last_price else f"{ticker} — нет цены"
    except Exception as e:
        return f"{ticker} — ошибка ({e})"

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
    return response.status_code == 200

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Ошибка: переменные TELEGRAM_TOKEN или TELEGRAM_CHAT_ID не заданы")
    else:
        tickers = ["MOEX", "MTSS", "X5"]
        prices = [get_price(ticker) for ticker in tickers]
        message = "\n".join(prices)
        print("Отправка сообщения:\n", message)
        send_telegram_message(token, chat_id, message)
