import sys

USDRUB = 75

def calculate_trade_size(ticker, acceptable_PERC_loss, last_close):
    if '.MM' in ticker:
        last_close = last_close / USDRUB
    trade_size = 5 / (acceptable_PERC_loss * last_close)
    return trade_size

if __name__ == '__main__':
    ticker = sys.argv[1]
    acceptable_PERC_loss = float(sys.argv[2])
    last_close = float(sys.argv[3])
    print(calculate_trade_size(ticker, acceptable_PERC_loss, last_close))
