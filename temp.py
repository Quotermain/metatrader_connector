from mysql.connector import connect
import pickle

with open('data/tickers/all_tickers.pickle', 'rb') as file:
    ALL_TICKERS = pickle.load(file)
CRIDENTIALS = {
    'host': 'localhost', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}
TO_INSERT = [(ticker, False) for ticker in ALL_TICKERS]

connection = connect(**CRIDENTIALS)
query = 'INSERT INTO is_signal_sent (ticker, is_sent) VALUES (%s, %s)'
with connection.cursor() as cursor:
    cursor.executemany(query, TO_INSERT)
    connection.commit()

connection.close()
