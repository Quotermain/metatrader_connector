from mysql.connector import connect
import sys

CRIDENTIALS = {
    'host': '192.168.0.103', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}

def set_signal_is_sent_flag(ticker):
    query = f'UPDATE is_signal_sent_mt5 SET is_sent = 1 WHERE ticker = "{ticker}"'
    connection = connect(**CRIDENTIALS)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

if __name__ == '__main__':
    ticker = sys.argv[1]
    set_signal_is_sent_flag(ticker)
