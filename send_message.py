import os
import requests

# Словарь с названиями облигаций и их ISIN
bonds = {
    "RU000A10A3Z4": {"name": "ГТЛК 2P-04", "buy_price": 100.0},
    "RU000A10ASC6": {"name": "Европлн1Р9", "buy_price": 100.0},
    "RU000A10AXX2": {"name": "Хромос Б3", "buy_price": 100.0},
    "RU000A10AYB6": {"name": "Аспэйс 1Р2", "buy_price": 100.0},
    "RU000A10B8C1": {"name": "ЛаймЗайм05", "buy_price": 100.0}
}

stocks = {
    "MOEX": 189.49,
    "VTBR": 100.50,
    "X5": 3245.94
}

def get_bond_price_percent(isin):
    url = f"https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities/{isin}.json"
    try:
        response = requests.get(url)
        data = response.json()
        secdata = data['marketdata']['data']
        columns = data['marketdata']['columns']
        if not secdata or not secdata[0]:
            return None
        last_index = columns.index("LAST")
        last_price = secdata[0][last_index]  # Цена в процентах от номинала
        return last_price
    except Exception as e:
        print(f"Ошибка получения цены для {isin}: {e}")
        return None

def get_stock_price(ticker):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json"
    try:
        response = requests.get(url)
        data = response.json()
        secdata = data['marketdata']['data']
        columns = data['marketdata']['columns']
        if not secdata or not secdata[0]:
            return None
        last_index = columns.index("LAST")
        last_price = secdata[0][last_index]
        return last_price
    except Exception as e:
        print(f"Ошибка получения цены для {ticker}: {e}")
        return None

def format_bond_line(name, current_price, buy_price):
    if current_price is None:
        return f"{name} — нет данных"
    change = current_price - buy_price
    sign = "+" if change >= 0 else "−"
    return f"{name} — {current_price:.2f}% / {buy_price:.2f}% / {sign}{abs(change):.2f}%"

def format_stock_line(ticker, current_price, buy_price):
    if current_price is None:
        return f"{ticker} — нет данных"
    change = ((current_price - buy_price) / buy_price) * 100
    sign = "+" if change >= 0 else "−"
    return f"{ticker} — {current_price:.2f} ₽ / {buy_price:.2f} ₽ / {sign}{abs(change):.2f}%"

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
            current_price = get_stock_price(ticker)
            stock_lines.append(format_stock_line(ticker, current_price, buy_price))

        bond_lines = []
        for isin, info in bonds.items():
            current_price = get_bond_price_percent(isin)
            bond_lines.append(format_bond_line(info["name"], current_price, info["buy_price"]))

        message = "📊 Акции:\n" + "\n".join(stock_lines) + "\n\n💵 Облигации:\n" + "\n".join(bond_lines)
        print("Отправка сообщения:\n", message)
        send_telegram_message(token, chat_id, message)
