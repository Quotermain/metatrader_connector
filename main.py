import pickle
import MetaTrader5 as mt5
from utils.get_candles import get_candles
from utils.send_message import send_message
from utils.check_signal_is_sent import check_signal_is_sent
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag
from utils.calculate_trade_size import calculate_trade_size
from utils.check_trade_conditions import check_trade_conditions
from utils.get_american_candles import get_american_candles

from datetime import datetime
from time import sleep

with open('data/tickers/rus_stocks.pickle', 'rb') as file:
    RUS_STOCKS = pickle.load(file)
with open('data/tickers/currencies.pickle', 'rb') as file:
    CURRENCIES = pickle.load(file)
with open('data/tickers/usa_stocks.pickle', 'rb') as file:
    USA_STOCKS = pickle.load(file)
ALL_TICKERS = RUS_STOCKS + CURRENCIES + USA_STOCKS

with open('data/thresholds/open_close_day_dif.pickle', 'rb') as file:
    dict_open_close_day_dif = pickle.load(file)
with open('data/thresholds/open_close_5min_dif.pickle', 'rb') as file:
    dict_open_close_5min_dif = pickle.load(file)

def run(ticker):
    if ticker not in USA_STOCKS:
        df_day = get_candles(ticker, 'mt5.TIMEFRAME_D1', 1)
        df_5min = get_candles(ticker, 'mt5.TIMEFRAME_M5', 2)
    else:
        df_day, df_5min = get_american_candles(ticker)

    print(df_day)
    print(df_5min)

    signal = check_trade_conditions(ticker, df_day, df_5min)

    if signal is not None:
        signal_is_sent = check_signal_is_sent(ticker)

        if not signal_is_sent:
            acceptable_PERC_loss = dict_open_close_5min_dif[ticker]
            last_close = df_5min.close[-1]
            trade_size = calculate_trade_size(
                ticker, acceptable_PERC_loss, last_close
            )
            direction = 'short' if signal == 'short' else 'long'
            send_message(ticker + ' ' + direction + ' ' + str(trade_size))
            cur_time = datetime.now().time()
            print(cur_time, ticker, direction, trade_size)
            set_signal_is_sent_flag(ticker)


if __name__ == '__main__':
    while True:
        for ticker in ALL_TICKERS:
            try:
                run(ticker)
            except (KeyError):
                continue
