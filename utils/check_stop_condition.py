#import MetaTrader5 as mt5
from get_positions import get_positions
from pickle import load

with open('data/thresholds/high_low_5min_dif.pickle', 'rb') as file:
    dict_high_low_5min_dif = load(file)

def check_stop_condition():
    positions = get_positions()

    price_open =
    dist_to_stop = dict_high_low_5min_dif[ticker] * 0.5 * price
    return positions

if __name__ == "__main__":
    print(check_stop_condition(ticker))
