import MetaTrader5 as mt5
from sys import argv
from pickle import load

with open('data/thresholds/high_low_5min_dif.pickle', 'rb') as file:
    dict_high_low_5min_dif = load(file)

def send_transaction(ticker, volume, direction):

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    ticker_info = mt5.symbol_info(ticker)
    dgts = ticker_info.digits
    point = ticker_info.point

    if direction == 'short':
        direction = mt5.ORDER_TYPE_SELL
        price = ticker_info.bid
        dist_to_stop = dict_high_low_5min_dif[ticker] * 0.5 * price
        stop_limit = round(price + dist_to_stop, dgts)
        take_profit = round(price - dist_to_stop, dgts)
    elif direction == 'long':
        direction = mt5.ORDER_TYPE_BUY
        price = ticker_info.ask
        dist_to_stop = dict_high_low_5min_dif[ticker] * 0.5 * price
        stop_limit = round(price - dist_to_stop, dgts)
        take_profit = round(price + dist_to_stop, dgts)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": volume,
        'type': direction,
        'price': price,
        'sl': stop_limit,
        'tp': take_profit,
        "deviation": 1,
        "type_time": mt5.ORDER_TIME_GTC
    }

    result = mt5.order_send(request)

    return result.comment, stop_limit, take_profit

if __name__ == '__main__':
    ticker, volume, direction = argv[1], float(argv[2]), argv[3]
    result = send_transaction(ticker, volume, direction)
    for item in result:
        print(item)
