from mysql.connector import connect
import sys

CRIDENTIALS = {
    'host': '192.168.0.100', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}
connection = connect(**CRIDENTIALS)

def drop_flag_signal_is_sent(ticker):
    query = f'UPDATE is_signal_sent_mt5 SET is_sent = 0 WHERE ticker = "{ticker}"'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

if __name__ == '__main__':
    ticker = sys.argv[1]
    drop_flag_signal_is_sent(ticker)
