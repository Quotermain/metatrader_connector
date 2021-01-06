import pickle
import MetaTrader5 as mt5
from utils.get_candles import get_candles
from utils.send_message import send_message
from utils.check_signal_is_sent import check_signal_is_sent
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag
from utils.calculate_trade_size import calculate_trade_size
from utils.get_positions import get_positions

from time import sleep

with open('data/tickers/all_tickers.pickle', 'rb') as file:
    ALL_TICKERS = pickle.load(file)

#Removes some assets because of conditions of the market
ALL_TICKERS = [ticker for ticker in ALL_TICKERS if ticker not in ('USDZAR', )]

with open('data/thresholds/open_close_day_dif.pickle', 'rb') as file:
    dict_open_close_day_dif = pickle.load(file)
with open('data/thresholds/high_low_5min_dif.pickle', 'rb') as file:
    dict_high_low_5min_dif = pickle.load(file)

while True:
    for ticker in ALL_TICKERS:
        try:

            df = get_candles(ticker, 'mt5.TIMEFRAME_D1', 1)
            open_close_day_dif = abs(df.open - df.close) / df.open
            cond_day = all(open_close_day_dif > dict_open_close_day_dif[ticker])

            df = get_candles(ticker, 'mt5.TIMEFRAME_M5', 2)
            high_low_5min_dif = (df.high - df.low) / df.low
            cond_5min = all(high_low_5min_dif < dict_high_low_5min_dif[ticker])

            if cond_day and cond_5min:
                signal_is_sent = check_signal_is_sent(ticker)
                if not signal_is_sent:
                    acceptable_PERC_loss = dict_high_low_5min_dif[ticker] * 0.5
                    last_close = df.close[-1]
                    trade_size = calculate_trade_size(
                        ticker, acceptable_PERC_loss, last_close
                    )
                    send_message(ticker + ' ' + str(trade_size))
                    print(ticker, trade_size)
                    set_signal_is_sent_flag(ticker)
        except (KeyError):
            continue
