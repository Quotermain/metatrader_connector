import pickle

data_path = 'data/thresholds/'

with open(data_path + 'open_close_week_dif_mean.pickle', 'rb') as file:
    open_close_week_dif_mean = pickle.load(file)
with open(data_path + 'open_close_week_dif_std.pickle', 'rb') as file:
    open_close_week_dif_std = pickle.load(file)

with open(data_path + 'open_close_day_dif_mean.pickle', 'rb') as file:
    open_close_day_dif_mean = pickle.load(file)
with open(data_path + 'open_close_day_dif_std.pickle', 'rb') as file:
    open_close_day_dif_std = pickle.load(file)

with open(data_path + 'open_close_hour_dif_mean.pickle', 'rb') as file:
    open_close_hour_dif_mean = pickle.load(file)
with open(data_path + 'open_close_hour_dif_std.pickle', 'rb') as file:
    open_close_hour_dif_std = pickle.load(file)

with open(data_path + 'open_close_5min_dif_mean.pickle', 'rb') as file:
    open_close_5min_dif_mean = pickle.load(file)
with open(data_path + 'open_close_5min_dif_std.pickle', 'rb') as file:
    open_close_5min_dif_std = pickle.load(file)

with open(data_path + 'open_close_1min_dif_mean.pickle', 'rb') as file:
    open_close_1min_dif_mean = pickle.load(file)
with open(data_path + 'open_close_1min_dif_std.pickle', 'rb') as file:
    open_close_1min_dif_std = pickle.load(file)

def check_trade_conditions(ticker, tf_day, tf_hour, tf_5min, tf_1min):

    THRESH_DAY = (
        open_close_hour_dif_mean[ticker]
    )
    THRESH_HOUR = (
        open_close_hour_dif_mean[ticker] +
        3 * open_close_hour_dif_std[ticker]
    )

    condition_short = tf_5min.RSI[-1] >= 70 and tf_1min.RSI[-1] >= 70 and (
            (
                (tf_day.close[-1] - tf_day.open[-1]) /
                tf_day.open[-1] >= 0
            )
        ) and (
            (
                (tf_hour.close[-1] - tf_hour.open[-1]) /
                tf_hour.open[-1] >= THRESH_HOUR
            )
        )
    condition_long = tf_5min.RSI[-1] <= 30 and tf_1min.RSI[-1] <= 30 and (
            (
                (tf_day.open[-1] - tf_day.close[-1]) /
                tf_day.open[-1] >= 0
            )
        ) and (
            (
                (tf_hour.open[-1] - tf_hour.close[-1]) /
                tf_hour.open[-1] >= THRESH_HOUR
            )
        )

    if condition_short:
        return 'sell'
    elif condition_long:
        return 'buy'
    else:
        return None

if __name__ == '__main__':
    pass
