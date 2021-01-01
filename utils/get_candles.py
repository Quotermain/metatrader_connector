import MetaTrader5 as mt5
from datetime import datetime
import pytz
import pandas as pd
import sys

def get_candles(ticker, timeframe, n_candles):
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    rates = mt5.copy_rates_from_pos(ticker, eval(timeframe), 0, n_candles)
    mt5.shutdown()
    rates_frame = pd.DataFrame(rates)
    # Sets timezone to Moscow time just for convinience
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame.set_index('time', inplace=True)
    rates_frame.index = rates_frame.index.tz_localize(tz='Etc/UTC')
    rates_frame.index = rates_frame.index.tz_convert('Europe/Moscow')
    return rates_frame

if __name__ == '__main__':
    ticker = sys.argv[1]
    timeframe = sys.argv[2]
    n_candles = int(sys.argv[3])
    print(get_candles(ticker, timeframe, n_candles))
