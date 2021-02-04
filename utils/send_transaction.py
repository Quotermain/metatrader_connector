import MetaTrader5 as mt5
from sys import argv
from time import sleep

def send_transaction(ticker, volume, type, price, thresh, digits):

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    acceptable_loss = round(thresh * price,  digits)

    if type == 'sell':
        type = mt5.ORDER_TYPE_SELL
        sl = price + acceptable_loss
        tp = price - acceptable_loss
    elif type == 'buy':
        type = mt5.ORDER_TYPE_BUY
        sl = price - acceptable_loss
        tp = price + acceptable_loss

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": volume,
        "sl": sl,
        "tp": tp,
        "deviation": 1,
        'type': type,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    result = mt5.order_send(request)

    if result is not None:
        return result.comment
    else:
        return result

if __name__ == '__main__':
    ticker, volume, direction, price, thresh, pts  = (
        argv[1], float(argv[2]), argv[3], float(argv[4]),
        float(argv[5]), int(argv[6])
    )
    print(price)
    result = send_transaction(ticker, volume, direction, price, thresh, pts)
    print(result)
