import os
import requests

stocks = {
    "MOEX": 195.88,
    "MTSS": 233.00,
    "X5": 3245.94
}

bonds = {
    "RU000A10A3Z4": 1000.00,  # ГТЛК 2P-04
    "RU000A10ASC6": 1000.00,  # Европлн1Р9
    "RU000A10AXX2": 1000.00,  # Хромос Б3
    "RU000A10AYB6": 1000.00,  # Аспэйс 1Р2
    "RU000A10B8C1": 1000.00   # ЛаймЗайм05
}

def get_price(ticker, board, market):
    url = f"https://iss.moex.com/iss/engines/stock/markets/{market}/boards/{board}/securities/{ticker}.json"
    try:
        response = requests.get(url)
        data = response.json()
        secdata = data['marketdata']['data']
        columns = data['marketdata']['columns']

        if not secdata or not secdata[0]:
            return None

        last_index = columns.index("LAST")
        last_price = secdata[0][last_index]
        return last_price if last_price else None
    except Exception as e:
        print(f"{ticker} — ошибка получения цены: {e}")
        return None

def format_line(ticker, current_price, buy_price):
    if current_price is None:
        return f"{ticker} — нет данных"
    
    change_percent = ((current_price - buy_price) / buy_price) * 100
    sign = "+" if change_percent >= 0 else "−"
    return f"{ticker} — {current_price:.2f} ₽ / {buy_price:.2f} ₽ / {sign}{abs(change_percent):.2f}%"

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
        print("Ошибка: TELEGRAM_TOKEN или TELEGRAM_CHAT_ID не заданы")
    else:
        stock_lines = []
        for ticker, buy_price in stocks.items():
            current_price = get_price(ticker, board="TQBR", market="shares")
            stock_lines.append(format_line(ticker, current_price, buy_price))

        bond_lines = []
        for ticker, buy_price in bonds.items():
            current_price = get_price(ticker, board="TQCB", market="bonds")
            bond_lines.append(format_line(ticker, current_price, buy_price))

        message = "📊 Акции:\n" + "\n".join(stock_lines) + "\n\n💵 Облигации:\n" + "\n".join(bond_lines)
        print("Отправка сообщения:\n", message)
        send_telegram_message(token, chat_id, message)
