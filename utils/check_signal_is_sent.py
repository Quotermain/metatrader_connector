from mysql.connector import connect
import sys

CRIDENTIALS = {
    'host': '192.168.0.100', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}
connection = connect(**CRIDENTIALS)

def check_signal_is_sent(ticker):
    query = f'SELECT is_sent FROM is_signal_sent_mt5 WHERE ticker="{ticker}"'
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]
    return result

if __name__ == '__main__':
    ticker = sys.argv[1]
    print(check_signal_is_sent(ticker))
