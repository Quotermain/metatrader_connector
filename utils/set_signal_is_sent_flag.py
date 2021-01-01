from mysql.connector import connect
import sys

CRIDENTIALS = {
    'host': 'localhost', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}
connection = connect(**CRIDENTIALS)

def set_signal_is_sent_flag(ticker):
    query = f'UPDATE is_signal_sent SET is_sent = 1 WHERE ticker = "{ticker}"'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

if __name__ == '__main__':
    ticker = sys.argv[1]
    set_signal_is_sent_flag(ticker)
