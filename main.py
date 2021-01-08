import pickle
import MetaTrader5 as mt5
from utils.get_candles import get_candles
from utils.send_message import send_message
from utils.check_signal_is_sent import check_signal_is_sent
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag
from utils.calculate_trade_size import calculate_trade_size
from utils.check_trade_conditions import check_trade_conditions

from datetime import datetime
from time import sleep

print()

with open('data/tickers/all_tickers.pickle', 'rb') as file:
    ALL_TICKERS = pickle.load(file)

with open('data/thresholds/open_close_day_dif.pickle', 'rb') as file:
    dict_open_close_day_dif = pickle.load(file)
with open('data/thresholds/open_close_5min_dif.pickle', 'rb') as file:
    dict_open_close_5min_dif = pickle.load(file)

while True:
    for ticker in ALL_TICKERS:
        try:

            df_day = get_candles(ticker, 'mt5.TIMEFRAME_D1', 1)
            df_5min = get_candles(ticker, 'mt5.TIMEFRAME_M5', 2)

            '''print((df_day.close[-1] - df_day.open[-1]) > 0)
            sleep(5)'''

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
        except (KeyError):
            continue
