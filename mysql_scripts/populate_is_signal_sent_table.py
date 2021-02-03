from mysql.connector import connect
import pickle

with open('data/tickers/rus_stocks.pickle', 'rb') as file:
    RUS_STOCKS = pickle.load(file)
with open('data/tickers/currencies.pickle', 'rb') as file:
    CURRENCIES = pickle.load(file)
with open('data/tickers/usa_stocks.pickle', 'rb') as file:
    USA_STOCKS = pickle.load(file)
with open('data/tickers/usa_volume_leaders.pickle', 'rb') as file:
    USA_VOLUME_LEADERS = pickle.load(file)
ALL_TICKERS = list(set(RUS_STOCKS + CURRENCIES + USA_STOCKS + USA_VOLUME_LEADERS))

CRIDENTIALS = {
    'host': '192.168.0.103', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}

for ticker in ALL_TICKERS:
    connection = connect(**CRIDENTIALS)
    query = f'INSERT INTO is_signal_sent_mt5 (ticker, is_sent) VALUES ("{ticker}", 0)'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
