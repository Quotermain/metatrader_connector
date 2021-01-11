from utils.get_candles import get_candles
from utils.send_message import send_message
from utils.check_signal_is_sent import check_signal_is_sent
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag
from utils.calculate_trade_size import calculate_trade_size
from utils.check_trade_conditions import check_trade_conditions
from utils.get_american_candles import get_american_candles
from utils.get_positions import get_positions
from utils.send_transaction import send_transaction

import pickle
import MetaTrader5 as mt5
from datetime import datetime
from time import sleep
from multiprocessing import Pool
import sys

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

    #print(ticker)

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    info = mt5.symbol_info(ticker)

    if ticker not in USA_STOCKS:
        df_day = get_candles(ticker, 'mt5.TIMEFRAME_D1', 1)
        df_5min = get_candles(ticker, 'mt5.TIMEFRAME_M5', 2)
    else:
        df_day = get_american_candles(ticker, '2d', '1d')
        df_5min = get_american_candles(ticker, '10m', '5m')

    '''if ticker in USA_STOCKS:
        print(ticker)
        print(df_day)
        print(df_5min)
        print()
        sleep(1)'''

    signal = check_trade_conditions(ticker, df_day, df_5min)

    if signal is not None:
        signal_is_sent = check_signal_is_sent(ticker)
        position = get_positions(ticker)

        if (not signal_is_sent) and (position is None):

            acceptable_PERC_loss = dict_open_close_5min_dif[ticker]
            last_close = df_5min.close[-1]
            trade_size = calculate_trade_size(
                ticker, acceptable_PERC_loss, last_close
            )
            contract_size = info.trade_contract_size
            min_volume = info.volume_min
            trade_size = round(trade_size / contract_size / min_volume)
            trade_size = trade_size * min_volume

            direction = 'sell' if signal == 'sell' else 'buy'
            send_message(ticker + ' ' + direction + ' ' + str(trade_size))
            print(send_transaction(ticker, trade_size, direction))
            cur_time = datetime.now().time()
            print(cur_time, ticker, direction, trade_size)
            set_signal_is_sent_flag(ticker)


if __name__ == '__main__':
    while True:
        with Pool(2) as p:
            try:
                p.map_async(run, ALL_TICKERS).get(30)
            except KeyboardInterrupt:
                print("Caught KeyboardInterrupt, terminating workers")
                p.terminate()
                p.join()
                break
            except Exception as e:
                print(e)
                send_message(e)
                p.terminate()
                p.join()
