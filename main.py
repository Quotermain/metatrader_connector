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
from technical_indicators_lib import RSI
import pandas as pd
pd.options.mode.chained_assignment = None

with open('data/tickers/rus_stocks.pickle', 'rb') as file:
    RUS_STOCKS = pickle.load(file)
with open('data/tickers/currencies.pickle', 'rb') as file:
    CURRENCIES = pickle.load(file)
with open('data/tickers/usa_stocks.pickle', 'rb') as file:
    USA_STOCKS = pickle.load(file)
with open('data/tickers/usa_volume_leaders.pickle', 'rb') as file:
    USA_VOLUME_LEADERS = pickle.load(file)
ALL_TICKERS = list(set(RUS_STOCKS + CURRENCIES + USA_STOCKS + USA_VOLUME_LEADERS))

data_path = 'data/thresholds/'

with open(data_path + 'open_close_5min_dif_mean.pickle', 'rb') as file:
    open_close_5min_dif_mean = pickle.load(file)
with open(data_path + 'open_close_5min_dif_std.pickle', 'rb') as file:
    open_close_5min_dif_std = pickle.load(file)

AGG_DICT = {
    'open': 'first', 'high': 'max', 'low': 'min',
    'close': 'last', 'volume': 'sum'
}

def run(ticker):

    #print(ticker)

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    info = mt5.symbol_info(ticker)

    if ticker not in USA_STOCKS:
        df_1min = get_candles(
            ticker, 'mt5.TIMEFRAME_M1', 5000
        ).loc[:, ['open', 'high', 'low', 'close', 'volume']]
    else:
        # Получаем с яху, потому что с МТ5 с 15 минутным лагом
        df_1min = get_american_candles(
            ticker, '3d', '1m'
        ).loc[:, ['open', 'high', 'low', 'close', 'volume']]
    df_5min = df_1min.resample('5Min').agg(AGG_DICT)
    df_hour = df_1min.resample('60Min').agg(AGG_DICT)
    df_day = df_1min.resample('1D').agg(AGG_DICT)

    rsi = RSI()
    df_1min = rsi.get_value_df(df_1min)
    df_5min = rsi.get_value_df(df_5min)

    signal = check_trade_conditions(ticker, df_day, df_hour, df_5min, df_1min)

    if signal is not None:
        signal_is_sent = check_signal_is_sent(ticker)
        position = get_positions(ticker)

        if (not signal_is_sent) and (position is None):

            acceptable_PERC_loss = (
                open_close_5min_dif_mean[ticker] +
                3 * open_close_5min_dif_std[ticker]
            )

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
            print(
                send_transaction(
                    ticker, trade_size, direction, last_close,
                    acceptable_PERC_loss, info.digits
                )
            )
            cur_time = datetime.now().time()
            print(cur_time, ticker, direction, trade_size)
            set_signal_is_sent_flag(ticker)


if __name__ == '__main__':
    while True:
        try:
            with Pool(4) as p:
                p.map(run, ALL_TICKERS)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            break
        except KeyError as e:
            print(e)
            continue
        except Exception as e:
            print(e)
            send_message(e)
            sleep(50000)
            continue
