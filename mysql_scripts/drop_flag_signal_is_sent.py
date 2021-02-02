from mysql.connector import connect
import sys
import pickle

CRIDENTIALS = {
    'host': '192.168.0.103', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}

with open('data/tickers/rus_stocks.pickle', 'rb') as file:
    RUS_STOCKS = pickle.load(file)
with open('data/tickers/currencies.pickle', 'rb') as file:
    CURRENCIES = pickle.load(file)
with open('data/tickers/usa_stocks.pickle', 'rb') as file:
    USA_STOCKS = pickle.load(file)
ALL_TICKERS = RUS_STOCKS + CURRENCIES + USA_STOCKS

def drop_flag_signal_is_sent(ticker):
    connection = connect(**CRIDENTIALS)
    if ticker == 'ALL':
        query = f'UPDATE is_signal_sent_mt5 SET is_sent = 0 WHERE is_sent = 1'
    else:
        query = f'UPDATE is_signal_sent_mt5 SET is_sent = 0 WHERE ticker = "{ticker}"'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

if __name__ == '__main__':
    ticker = sys.argv[1]
    drop_flag_signal_is_sent(ticker)
