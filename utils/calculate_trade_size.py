from utils.get_candles import get_candles
import sys

def calculate_trade_size(ticker, acceptable_PERC_loss, last_close):
    if '.MM' in ticker:
        USDRUB = get_candles('USDRUB', 'mt5.TIMEFRAME_M5', 1).close[0]
        last_close = last_close / USDRUB
    trade_size = 10 / (acceptable_PERC_loss * last_close)
    return trade_size

if __name__ == '__main__':
    ticker = sys.argv[1]
    acceptable_PERC_loss = float(sys.argv[2])
    last_close = float(sys.argv[3])
    print(calculate_trade_size(ticker, acceptable_PERC_loss, last_close))
