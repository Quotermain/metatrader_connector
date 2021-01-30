import MetaTrader5 as mt5
from sys import argv

def send_transaction(ticker, volume, type):

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    if type == 'sell':
        type = mt5.ORDER_TYPE_SELL
    elif type == 'buy':
        type = mt5.ORDER_TYPE_BUY

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": volume,
        'type': type,
        "type_time": mt5.ORDER_TIME_GTC
    }

    result = mt5.order_send(request)

    if result is not None:
        return result.comment
    else:
        return

if __name__ == '__main__':
    ticker, volume, direction = argv[1], float(argv[2]), argv[3]
    print(volume)
    result = send_transaction(ticker, volume, direction)
    print(result)
